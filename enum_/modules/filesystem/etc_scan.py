import os
import stat
import subprocess


def etc_scan():

	output = []

	for root , dirs , files in os.walk("/etc/"):
		for etc_file in files:
			path = os.path.join(root, etc_file)

			if os.path.islink(path):
				continue

			try:
				mode = os.stat(path).st_mode
			except (FileNotFoundError, PermissionError):
				continue

			world_writable = bool(mode & stat.S_IWOTH)
			world_readable = bool(mode & stat.S_IROTH)

			if world_writable:
				output.append(path)
			elif (etc_file == "shadow") and world_readable:
				output.append(path)


	if not output:
		output = "Nothing"
	else:
		output = subprocess.run(["ls", "-ldh", *output], text=True, capture_output=True).stdout.strip()

	raw = {
		"Output": output
	}

	return raw