import sys
import argparse
from shared.look.colors import *


def positive_float(value):
    value = float(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("--interval must be greater than 0")
    return value


def module_choice():
    mode = "enum"

    if len(sys.argv) == 1:
        enum_args = []
    else:
        enum_args = sys.argv[1:]

    if len(sys.argv) > 1 and sys.argv[1] in ("org", "organizer"):

        organizer_parser = argparse.ArgumentParser(
            prog="riff.py org",
            description="Riff Organizer: interactive checklist/notes mode. "
                        "Set RIFF_TEMPLATE_PATH environment variable to use a JSON template file.",
            formatter_class=argparse.RawTextHelpFormatter
        )

        organizer_parser.add_argument("--item", "-i", type=int, help="Select checklist item by index")
        organizer_parser.add_argument("--category", "-c", help="Set or update checklist item category")
        organizer_parser.add_argument("--question", "-q", help="Set or update checklist item question")
        organizer_parser.add_argument("--notes", "-n", help="Set or update checklist item notes")
        organizer_parser.add_argument("--hints", "-H", help="Set or update checklist item command hints")
        organizer_parser.add_argument("--status", "-s", choices=["found", "not found", "unchecked"],help="Set or update checklist item status")
        organizer_parser.add_argument("--remove", "-r", action="store_true", help="Remove selected checklist item")
        organizer_parser.add_argument("--add", "-a", action="store_true", help="Add a new checklist item")

        return "org" , organizer_parser.parse_args(sys.argv[2:])

    elif len(sys.argv) > 1 and sys.argv[1] in ("mon", "pmon"):

        pmon_parser = argparse.ArgumentParser(
            prog="riff.py pmon",
            description="Riff pmon: real-time process monitor for catching privesc-relevant activity (cron jobs, spawned processes, reverse shells) using a hybrid inotify + polling approach, inotify "
                        "watches on filesystem activity trigger immediate /proc scans, backed by regular polling as a fallback. "
                        "Very short-lived processes (a few ms) may still be missed. Use --interval to tune the polling fallback speed, and --watch/--watch-flat/--watch-only to customize monitored directories.",
            formatter_class=argparse.RawTextHelpFormatter
        )

        pmon_parser.add_argument("--interval", "-I", type=positive_float, default=0.05 ,help="Poll interval in seconds (default: 0.05), lower catches shorter processes but uses more CPU.")
        pmon_parser.add_argument("--watch", "-w", nargs='+',help="Additional directories to watch recursively (besides the defaults)")
        pmon_parser.add_argument("--watch-flat", nargs='+',help="Additional directories to watch non-recursively (besides the defaults)")
        pmon_parser.add_argument("--watch-only", nargs='+',help="Replace default recursive watch dirs entirely with this list")


        return "pmon", pmon_parser.parse_args(sys.argv[2:])

    else:

        if enum_args and enum_args[0] == "enum":
            enum_args = enum_args[1:]

        enum_parser = argparse.ArgumentParser(
            description=f"""
Riff: targeted Linux privilege escalation enumeration tool,
a personal alternative for other tools.

Available modes:
  riff.py            Run the full enumeration scan (default mode)
  riff.py org        Run the organizer (checklist/notes) mode
  riff.py pmon       Run the process monitor mode.

  Each module output is checked against a rule set and findings
  are classified into DIRECT_ROOT, RISKY_CONFIG, FLAGGED_SECRET,
  NEEDS_REVIEW, and EXPECTED tiers, colored accordingly. Use
  --summary for a condensed, severity-sorted report of every
  finding across all modules, separate from the full per-module
  output.

  {BG_BLUE}WARNINGS:{RESET}
    {BG_CYAN}- BY DEFAULT RUNS ALL MODULES{RESET}
    {BG_CYAN}- IF RIFF ASKS FOR A PASSWORD AND YOU DON'T KNOW IT, PRESS ENTER TO SKIP; OTHER MODULES WILL CONTINUE{RESET}
    {BG_CYAN}- FIRST RUN WILL BE LONGER (1 min) NEXT ARE AROUND 9 sec{RESET}

  Includes references to my favorites bands.

Available modules:
  sys_info         System information
  net_info         Network information
  user_info        Current user information (id, groups)
  env_info         Environment variables
  users_enum       System users (regular vs UID 0 super users)
  sudo_enum        sudo -l output
  etc_scan         World-readable/writable files in /etc
  ps_enum          Dumps `ps -eo pid,ppid,ruser,rgroup,args ww --forest`
  ssh_check        Checks SSH config for basic misconfigurations
  ftp_check        Checks FTP config for basic misconfigurations
  home_scan        Targeted home directory scan (SSH keys, folders, shell history — not a full directory dump)
  cron_enum        Looks for cronjobs
  cap_enum         Linux capabilities scan
  suid_enum        SUID binaries
  sgid_enum        SGID binaries
  nfs_check        Shows '/etc/exports', as fallback showmount -e localhost (no_root_squash check)
  session_check    Shows currently logged users.
	""",
            formatter_class=argparse.RawTextHelpFormatter
        )

        enum_parser.add_argument("--skip-loading", action="store_true", help="Skip the loading bar animation")
        enum_parser.add_argument("--modules", "-m", nargs="+", help="Run only specific modules (space separated names)")
        enum_parser.add_argument("--exclude", "-x", nargs="+", help="Exclude modules from the run (space separated names)")
        enum_parser.add_argument("--fast", "-f", action="store_true",help="Skip suids/sgids and capabilities.")
        enum_parser.add_argument("--summary", action="store_true", help="Shows summary")
        enum_parser.add_argument("--default", default=False , action="store_true", help="Shows default suids/sgids. (Default OFF)")
        enum_parser.add_argument("--output", "-o", help="Write output to a file")
        enum_parser.add_argument("--verbose", "-v", action="store_true", help="Turn off line limit per module. Potentially very messy/long output")
        enum_parser.add_argument("--silent", "-s", action="store_true", help="Turn off module output shows only summary")
        enum_parser.add_argument("--trim", "-t", type=int , default=45 , help="Amount of line shown before trimming module output (Default 45, doesnt affect small modules that produce few lines)")
        enum_parser.add_argument("--password", "-p", help="Password for sudo")
        enum_parser.add_argument("--no-colors", action="store_true", default=False, help="Print output without ANSI colors")

        return "enum" , enum_parser.parse_args(enum_args)