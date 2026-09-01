from enum_.shared.utils import run_command

def network():

	ip_a = run_command(['ip', 'a'])
	ss_tuln = run_command(['ss', '-tuln'])

	try:
		with open('/etc/hosts', 'r') as etc_hosts:
			hosts = etc_hosts.read().strip()
	except (FileNotFoundError, PermissionError):
		hosts = "---"

	return {
		"/etc/hosts": hosts,
		"ip a": ip_a,
		"ss -tuln": ss_tuln,
	}
