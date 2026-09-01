from enum_.shared.utils import run_command

def system() -> tuple:

	hostname = run_command(['hostname'])
	kernel_release = run_command(['uname', '-r'])
	architecture = run_command(['uname', '-m'])

	try:
		with open("/etc/issue", encoding='UTF-8') as etc_issue:
			pretty_name = etc_issue.read().replace(r'\n \l', '').strip()
	except (FileNotFoundError, PermissionError):
		pretty_name = "N/A (Couldn't read /etc/issue)"

	raw = {
		"HOST": hostname,
		"KERNEL": kernel_release,
		"ARCH": architecture,
		"OS": pretty_name
	}

	return raw
