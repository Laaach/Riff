import os
import time
import sys
from datetime import datetime
from inotify_simple import INotify , flags
from shared.look.colors import *


def _parse_stat(stat):
    command_end = stat.rfind(")")

    if command_end == -1:
        return None

    stat_splitted = stat[command_end + 2:].split()

    if len(stat_splitted) < 20:
        return None

    return int(stat_splitted[19])

def _process_start_ticks(pid):
    try:
        with open(f"/proc/{pid}/stat") as stat_file:
            stat = stat_file.read()
    except (FileNotFoundError, PermissionError, ProcessLookupError):
        return None

    return _parse_stat(stat)


def _format_start_time(start_ticks, uptime, tps):
    start_seconds_after_boot = start_ticks / tps
    boot_time = time.time() - uptime
    process_start = boot_time + start_seconds_after_boot
    return datetime.fromtimestamp(process_start).strftime("%H:%M:%S")


def _get_process_info(pid):

    try:
        with open(f"/proc/{pid}/cmdline") as cmdline_file:
            cmdline = (cmdline_file.read().replace("\x00", " ").strip())

        with open(f"/proc/{pid}/status") as status_file:
            status = status_file.read().splitlines()

    except (FileNotFoundError, PermissionError , OSError, ProcessLookupError):
        return None

    if not cmdline:
        return None

    ruid = rgid = ppid = "?"

    for line in status:

        if line.startswith("Uid:"):
            ruid = line.split()[1]

        elif line.startswith("Gid:"):
            rgid = line.split()[1]

        elif line.startswith("PPid:"):
            ppid = line.split()[1]

    return {
        "cmdline": cmdline,
        "ruid": ruid,
        "rgid": rgid,
        "ppid": ppid
    }

def _warmup_processes_seen():
    processes_seen = {}

    with os.scandir("/proc") as proc:
        for entry in proc:
            if not entry.name.isdigit():
                continue

            try:
                start_ticks = _process_start_ticks(entry.name)
            except ProcessLookupError:
                continue
            if start_ticks is not None:
                processes_seen[entry.name] = start_ticks

    return processes_seen


def _add_recursive_watch(inotify, path, watch_paths):
    try:
        wd = inotify.add_watch(path, flags.CREATE | flags.OPEN | flags.ACCESS)
        watch_paths[wd] = path
    except (PermissionError, FileNotFoundError):
        return

    try:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    _add_recursive_watch(inotify, entry.path, watch_paths)
    except (PermissionError, NotADirectoryError):
        pass


def _add_flat_watch(inotify, path, watch_paths):
    try:
        wd = inotify.add_watch(path, flags.CREATE | flags.OPEN | flags.ACCESS)
        watch_paths[wd] = path
    except (PermissionError, FileNotFoundError):
        pass


def _setup_watches(inotify, recursive_dirs , flat_dirs):
    watch_paths = {}

    for path in recursive_dirs:
        _add_recursive_watch(inotify, path, watch_paths)

    for path in flat_dirs:
        _add_flat_watch(inotify, path, watch_paths)

    return watch_paths

def _scan_proc(processes_seen, ticks_per_second, output_for_summary):
    current_processes = set()



    with open("/proc/uptime") as f:
        uptime = float(f.read().split()[0])

    try:
        with os.scandir("/proc") as proc:

            for entry in proc:

                if not entry.name.isdigit():
                    continue

                pid = entry.name
                current_processes.add(pid)

                start_ticks = _process_start_ticks(pid)

                if start_ticks is None:
                    continue

                if processes_seen.get(pid) == start_ticks:
                    continue

                processes_seen[pid] = start_ticks

                process_start = _format_start_time(start_ticks, uptime, ticks_per_second)

                info = _get_process_info(pid)

                if info is None:
                    continue

                line = (
                    f"{DARK_GRAY}[{process_start}]{RESET} "
                    f"{CYAN}pid={pid:<7}{RESET}"
                    f"{CYAN}ppid={info['ppid']:<7}{RESET}"
                    f"{CYAN}user={str(info['ruid']) + ':' + str(info['rgid']):<11}{RESET}"
                    f"→ {info['cmdline']}"
                )

                print(line)
    except PermissionError:
        pass

    return {pid: start for pid, start in processes_seen.items() if pid in current_processes}


def pmon(interval, recursive_dirs, flat_dirs):
    processes_seen = _warmup_processes_seen()
    output_for_summary = []

    ticks_per_second = os.sysconf(os.sysconf_names["SC_CLK_TCK"])

    inotify = INotify()
    try:
        watch_paths = _setup_watches(inotify, recursive_dirs , flat_dirs)
    except OSError:
        sys.exit("Paths contain too many files.")
    timeout_ms = int(interval * 1000)

    try:
        while True:
            inotify.read(timeout=timeout_ms)
            processes_seen = _scan_proc(processes_seen, ticks_per_second, output_for_summary)

    except KeyboardInterrupt:
        sys.exit()