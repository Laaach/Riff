import os
import subprocess

def cron_enum():

    cron_jobs_found = []

    try:
        with os.scandir('/var/spool/cron/crontabs/') as cron_files:
            for cron_file in cron_files:
                if not cron_file.is_dir():
                    try:
                        with open(cron_file.path, 'r') as cron_file_content:
                            for line in cron_file_content.readlines():
                                line = line.strip()
                                if not line or line[0] == "#":
                                    continue
                                if line.startswith("@") or line[0].isdigit() or line[0] == "*":
                                    cron_jobs_found.append(f"{line} <-- FOUND IN {cron_file.path}")   
                    except (PermissionError, UnicodeDecodeError):
                        pass
    except (FileNotFoundError, PermissionError, NotADirectoryError):
        pass

    try:
        with open("/etc/crontab", 'r') as etc_crontab:
            for line in etc_crontab.readlines():
                line = line.strip()
                if not line or line[0] == "#":
                    continue
                if line.startswith("@") or line[0].isdigit() or line[0] == "*":
                    cron_jobs_found.append(f"{line} <-- FOUND IN /etc/crontab")
    except (PermissionError, FileNotFoundError):
        pass

    try:
        other_cron_files = subprocess.run(
            ["ls", "-alh", "/etc/cron.d/", "/etc/cron.daily/", "/etc/cron.hourly/", "/etc/cron.weekly/","/etc/cron.monthly/"], capture_output=True, text=True).stdout.strip()
    except (FileNotFoundError, PermissionError, NotADirectoryError):
        other_cron_files = f"Failed to list cron directories"

    cron_jobs_found = '\n'.join(cron_jobs_found)

    raw = {
        "CRON JOBS": cron_jobs_found,
        "OTHER CRON FILES": other_cron_files
    }

    return raw