import subprocess
from enum_.modules.privileges.shared.logic import filter_suid_sgid

default_suids = [
	"/usr/bin/passwd",
	"/usr/bin/su",
	"/usr/bin/sudo",
	"/usr/bin/mount",
	"/usr/bin/umount",
	"/usr/bin/newgrp",
	"/usr/bin/gpasswd",
	"/usr/bin/chsh",
	"/usr/bin/chfn",
	"/usr/bin/fusermount",
	"/usr/bin/fusermount3",
	"/usr/bin/pkexec",
	"/usr/bin/ping",
	"/usr/lib/openssh/ssh-keysign",
	"/usr/lib/dbus-1.0/dbus-daemon-launch-helper",
	"/usr/sbin/pppd",
	"/usr/sbin/mount.cifs",
	"/usr/sbin/mount.nfs",
	"/usr/sbin/exim4",
	"/usr/lib/xorg/Xorg.wrap",
]


def suid(show_default):
    suids, _ = filter_suid_sgid()

    if not show_default:
        suids = [suid for suid in suids if suid not in default_suids]

    suid_outputs = []

    if suids:
        result = subprocess.run(["ls", "-ldh", *suids], text=True, capture_output=True)
        if result.stdout.strip():
            suid_outputs.append(result.stdout.strip())

    raw = {"SUIDS": "\n".join(suid_outputs)}

    return raw



