from core.look.loading import loading
from enum_.modules.filesystem import home, etc
from enum_.modules.privileges import sudo, capabilities, suid, sgid
from enum_.modules.services import cron, ssh, ftp
from enum_.modules.system import system, environment, processes, path
from enum_.modules.users import identity, users, sessions
from enum_.modules.network import network, nfs
from shared.look.colors import *
import sys

def registry(is_fast, modules, exclude, skip_loading, show_default, password):

    modules_list = {
        'loading': lambda: loading(is_fast),
        'system': lambda: system.system(),
        'identity': lambda: identity.identity(),
        'network': lambda: network.network(),
        'environment': lambda: environment.environment(),
        'users': lambda: users.users(),
        'sudo': lambda: sudo.sudo(password),
        'etc': lambda: etc.etc(),
        'processes': lambda: processes.processes(),
        'ssh': lambda: ssh.ssh(),
        'ftp': lambda: ftp.ftp(),
        'nfs': lambda: nfs.nfs(),
        'cron': lambda: cron.cron(),
        'home': lambda: home.home(),
        'capabilities': lambda: capabilities.capabilities(),
        'suid': lambda: suid.suid(show_default),
        'sgid': lambda: sgid.sgid(show_default),
        'sessions': lambda: sessions.sessions(),
        'path': lambda: path.path()
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
        modules_to_run.pop("suid", None)
        modules_to_run.pop("sgid", None)
        modules_to_run.pop("capabilities", None)

    modules_to_run["loading"] = lambda: loading(is_fast)

    if skip_loading:
        modules_to_run.pop("loading")

    return modules_to_run