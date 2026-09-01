from enum_.modules.services.shared.logic import scan_config

def ftp():

    vsftpd = scan_config('/etc/vsftpd.conf')
    proftpd = scan_config('/etc/proftpd/proftpd.conf')

    raw = {
        "vsftpd": vsftpd,
        "proftpd": proftpd
    }

    return raw