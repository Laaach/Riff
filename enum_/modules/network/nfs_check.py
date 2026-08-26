import subprocess

def nfs_check():
	try:
		with open('/etc/exports', 'r') as exports_file:
			content = exports_file.read().strip()
	except (FileNotFoundError, PermissionError):
		content = ""

	if not content:
		try:
			result = subprocess.run(['showmount', '-e', 'localhost'], capture_output=True, text=True, timeout=6)
			content = result.stdout.strip() if result.returncode == 0 else "showmount failed or no exports"
		except subprocess.TimeoutExpired:
			content = "showmount timed out (NFS service likely not responding)"
		except FileNotFoundError:
			content = "showmount not installed, no NFS exports found"

	raw = {
		"NFS Exports": content
	}

	return raw
