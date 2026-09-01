import os
def _users_from_etc_passwd():
	users_homes = []

	bad_shells = ['/bin/sync', '/bin/false', '/usr/sbin/nologin', '/sbin/nologin', '/bin/nologin', '/bin/true']
	bad_homes = ["/", "", "/var", "/dev", "/proc", "/sys"]

	with open("/etc/passwd", 'r', encoding='UTF-8') as etc_passwd:
		etc_passwd = etc_passwd.readlines()

	for line in etc_passwd:
		line = line.strip().split(':')

		if (user_shell := line[6]) in bad_shells or (user_home := line[5]) in bad_homes:
			continue

		users_homes.append(line[5])

	return users_homes


def _is_history_file(file):
	return file in [".bash_history", ".zsh_history", ".mysql_history"]


def _is_private_key(path):
	private_keys_markers = ["-----BEGIN OPENSSH PRIVATE KEY-----", "-----BEGIN RSA PRIVATE KEY-----",
	                        "-----BEGIN DSA PRIVATE KEY-----", "-----BEGIN EC PRIVATE KEY-----",
	                        "-----BEGIN PGP PRIVATE KEY BLOCK-----", "-----BEGIN PRIVATE KEY-----",
	                        "-----BEGIN ENCRYPTED PRIVATE KEY-----"]

	try:
		with open(path, 'r', errors='ignore') as f:
			content = f.read()
	except (FileNotFoundError, PermissionError, IsADirectoryError):
		return False

	return any(marker in content for marker in private_keys_markers)


def _home_folder_scan():
	ssh_folders = []
	history_files = []
	private_keys = []

	for user_home in _users_from_etc_passwd():

		for root, dirs, files in os.walk(user_home):

			for d in dirs:
				dir_path = os.path.join(root, d)

				if d == ".ssh":
					ssh_folders.append(dir_path)

			for f in files:
				file_path = os.path.join(root, f)

				if _is_history_file(f):
					history_files.append(f"{file_path}")

	for ssh_folder in ssh_folders:
		try:
			with os.scandir(ssh_folder) as ssh_content:
				for entry in ssh_content:
					if entry.is_dir():
						continue
					if _is_private_key(entry.path):
						private_keys.append(f"{entry.path} <-- SSH PRIVATE KEY FOUND")
		except (FileNotFoundError, PermissionError, NotADirectoryError):
			pass

	return ssh_folders, history_files, private_keys


def home():
	ssh_folders, history_files, private_keys = _home_folder_scan()

	ssh_folders_str = "\n".join(ssh_folders)
	history_files_str = "\n".join(history_files)
	private_keys_str = "\n".join(private_keys)

	raw = {
		"SSH Folders": ssh_folders_str,
		"History Files": history_files_str,
		"Private Keys": private_keys_str
	}

	return raw