from core.look.loading import loading
from enum_.modules.filesystem import home_scan, etc_scan
from enum_.modules.privileges import sudo_enum, cap_enum, suid_enum, sgid_enum
from enum_.modules.services import cron_enum , ssh_check , ftp_check
from enum_.modules.system import sys_info, env_info, ps_enum
from enum_.modules.users import user_info, users_enum, session_check
from enum_.modules.network import net_info, nfs_check
from shared.look.colors import *
import sys

def registry(is_fast, modules, exclude, skip_loading, show_default, password):

    modules_list = {
        'loading': lambda: loading(is_fast),
        'sys_info': lambda: sys_info.sys_info(),
        'user_info': lambda: user_info.user_info(),
        'net_info': lambda: net_info.net_info(),
        'env_info': lambda: env_info.env_info(),
        'users_enum': lambda: users_enum.users_enum(),
        'sudo_enum': lambda: sudo_enum.sudo_enum(password),
        'etc_scan': lambda: etc_scan.etc_scan(),
        'ps_enum': lambda: ps_enum.ps_enum(),
        'ssh_check': lambda: ssh_check.ssh_check(),
        'ftp_check': lambda: ftp_check.ftp_check(),
        'nfs_check': lambda: nfs_check.nfs_check(),
        'cron_enum': lambda: cron_enum.cron_enum(),
        'home_scan': lambda: home_scan.home_scan(),
        'cap_enum': lambda: cap_enum.cap_enum(),
        'suid_enum': lambda: suid_enum.suid_enum(show_default),
        'sgid_enum': lambda: sgid_enum.sgid_enum(show_default),
        'session_check': lambda: session_check.session_check()
    }

    if not modules:
        modules_to_run = dict(modules_list)
    else:
        invalid = [module for module in modules if module not in modules_list]
        if invalid:
            sys.exit(f"{BOLD_RED}Wrong module(s): {', '.join(invalid)}{RESET}")

        modules_to_run = {module: modules_list[module] for module in modules}

    if exclude:
        invalid_exclude = [module for module in exclude if module not in modules_list]
        if invalid_exclude:
            sys.exit(f"{BOLD_RED}Wrong exclude module(s): {', '.join(invalid_exclude)}{RESET}")
        for module in exclude:
            modules_to_run.pop(module, None)

    if is_fast:
        modules_to_run.pop("suid_enum", None)
        modules_to_run.pop("sgid_enum", None)
        modules_to_run.pop("cap_enum", None)

    modules_to_run["loading"] = lambda: loading(is_fast)

    if skip_loading:
        modules_to_run.pop("loading")

    display_names = {
        "home_scan": "Home Scan",
        "sys_info": "Sys Info",
        "user_info": "User Info",
        "net_info": "Net Info",
        "env_info": "Env Info",
        "users_enum": "Users Enum",
        "sudo_enum": "Sudo Enum",
        "etc_scan": "Etc Scan",
        "ps_enum": "Ps Enum",
        "ssh_check": "SSH Check",
        "ftp_check": "FTP Check",
        "nfs_check": "NFS Check",
        "cron_enum": "Cron Enum",
        "cap_enum": "Cap Enum",
        "suid_enum": "SUID Enum",
        "session_check": "Session Check",
    }


    modules_to_run = {
        display_names.get(module_name, module_name): function
        for module_name, function in modules_to_run.items()
    }

    return modules_to_run