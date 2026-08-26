from enum_.modules.privileges.shared.logic import filter_suid_sgid
import subprocess

default_sgids = [
    "/usr/bin/wall",
    "/usr/bin/write",
    "/usr/bin/ssh-agent",
    "/usr/bin/expiry",
    "/usr/bin/chage",
    "/usr/bin/crontab",
    "/usr/sbin/unix_chkpwd",
    "/usr/lib/x86_64-linux-gnu/utempter/utempter",
    "/usr/lib/mc/cons.saver",
    "/usr/lib/w3m/w3mimgdisplay",
    "/usr/lib/xorg/Xorg.wrap",
]

def sgid_enum(show_default):
    _, sgids = filter_suid_sgid()

    if not show_default:
        sgids = [sgid for sgid in sgids if sgid not in default_sgids]

    sgid_outputs = []

    if sgids:
        result = subprocess.run(["ls", "-ldh", *sgids], text=True, capture_output=True)
        if result.stdout.strip():
            sgid_outputs.append(result.stdout.strip())

    raw = {"SGIDS": "\n".join(sgid_outputs)}

    return raw