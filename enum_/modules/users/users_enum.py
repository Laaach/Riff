def users_enum():

	users = []
	super_users = []

	try:
		with open("/etc/passwd", 'r') as etc_passwd:
			etc_passwd = etc_passwd.readlines()
	except (FileNotFoundError, PermissionError):
		return {"ERROR": "Cant read /etc/passwd"}

	for line in etc_passwd:
		line = line.strip().split(':')

		if line[6] not in ['/usr/sbin/nologin', '/bin/sync', '/bin/false', '/sbin/nologin']:
			if line[2] == '0':
				super_users.append(line[0])
			else:
				users.append(line[0])

	raw = {
		"USERS": ', '.join(users),
		"SUPER USERS": ', '.join(super_users)
	}

	return raw
