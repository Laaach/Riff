import os
import subprocess
from enum_.core.output.file_presenter import present
from enum_.shared.utils import remove_comments_and_blanks


def _is_cron_job(line):
    return line.startswith("@") or line[0].isdigit() or line.startswith("*")

def _get_cron_jobs_from_file(file_path):
    cron_jobs = []

    try:
        with open(file_path, "r") as cron_file:
            cron_lines = remove_comments_and_blanks(cron_file)
            for cron_line in cron_lines:
                if _is_cron_job(cron_line):
                    cron_jobs.append(f"{cron_line} <-- FOUND IN {file_path}")
    except (OSError, UnicodeDecodeError):
        pass

    return cron_jobs

def _get_cron_directory_listings():
    cron_directories = [
        "/etc/cron.d/",
        "/etc/cron.daily/",
        "/etc/cron.hourly/",
        "/etc/cron.weekly/",
        "/etc/cron.monthly/",
    ]

    directory_listings = []

    for cron_directory in cron_directories:
        try:
            for cron_file in os.scandir(cron_directory):
                directory_listings.append(present(cron_file.path))
        except OSError:
            pass

    return directory_listings

def _get_user_crontab():
    try:
        crontab_output = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout.strip()
        return "\n".join(remove_comments_and_blanks(crontab_output.splitlines()))
    except OSError:
        return "Failed to list user cron jobs"

def cron():
    cron_jobs = []

    try:
        with os.scandir("/var/spool/cron/crontabs/") as crontab_files:
            for crontab_file in crontab_files:
                if not crontab_file.is_dir():
                    cron_jobs.extend(_get_cron_jobs_from_file(crontab_file.path))
    except OSError:
        pass

    cron_jobs.extend(_get_cron_jobs_from_file("/etc/crontab"))

    cron_directory_listings = _get_cron_directory_listings()

    user_crontab = _get_user_crontab()

    return {
        "\nCrontab -l": user_crontab,
        "\nCRON JOBS": "\n".join(cron_jobs),
        "\nOTHER CRON FILES": "\n".join(cron_directory_listings),
    }