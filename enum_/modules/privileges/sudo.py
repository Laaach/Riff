from enum_.shared.utils import run_command
from enum_.shared.utils import remove_comments_and_blanks
import os


def sudo(password):

    try:
        with open("/etc/sudoers") as sudoers_file:
            sudoers_content = "\n".join(remove_comments_and_blanks(sudoers_file))
    except (FileNotFoundError, PermissionError):
        sudoers_content = "Permission denied"

    try:
        sudoers_d_listings = []

        for sudoers_d_entry in os.scandir("/etc/sudoers.d/"):
            if sudoers_d_entry.is_file():
                with open(sudoers_d_entry.path) as sudoers_file:
                    sudoers_d_listings.append(f"▸ {sudoers_d_entry.path}\n"+ "\n".join(remove_comments_and_blanks(sudoers_file)))
    except (FileNotFoundError, PermissionError):
        sudoers_d_listings = ["Permission denied"]

    if password:
        sudo_list = run_command(["sudo", "-lS"], input_text=password + "\n")
    else:
        sudo_list = "Password not provided, if you know it run Riff with -p [PASSWORD]"

    return {
        "\nSudo List": sudo_list,
        "\n/etc/sudoers": sudoers_content,
        "\n/etc/sudoers.d": "\n\n".join(sudoers_d_listings)
    }
