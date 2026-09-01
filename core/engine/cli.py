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

  Includes references to my favorites bands.

Available modules:
    Use --list-modules to see a list of available modules
	""",
            formatter_class=argparse.RawTextHelpFormatter
        )

        enum_parser.add_argument("--modules", "-m", nargs="+", help="run only specific modules (space separated)")
        enum_parser.add_argument("--exclude", "-x", nargs="+", help="exclude modules from the run (space separated)")
        enum_parser.add_argument("--fast", "-f", action="store_true", help="skip SUIDs, SGIDs and capabilities")
        enum_parser.add_argument("--output", "-o", help="write output to a file")
        enum_parser.add_argument("--verbose", "-v", action="store_true", help="disable line limit per module")
        enum_parser.add_argument("--silent", "-s", action="store_true", help="show only summary")
        enum_parser.add_argument("--trim", "-t", type=int, default=45, help="lines shown before trimming (default: 45)")
        enum_parser.add_argument("--password", "-p", help="password for sudo")
        enum_parser.add_argument("--skip-loading", action="store_true", help="skip the loading bar animation")
        enum_parser.add_argument("--summary", action="store_true", help="show summary")
        enum_parser.add_argument("--list-modules", action="store_true", default=False , help="show available modules")
        enum_parser.add_argument("--no-colors", action="store_true", default=False, help="disable ANSI colors")

        return "enum" , enum_parser.parse_args(enum_args)