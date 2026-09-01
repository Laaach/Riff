from enum_.modules.services.shared.logic import scan_config

def ssh():
    sshd = scan_config('/etc/ssh/sshd_config')

    raw = {
        "sshd": sshd,
    }

    return raw