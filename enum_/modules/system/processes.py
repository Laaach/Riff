from enum_.shared.utils import run_command

def processes():

	output = run_command(['ps', '-eo', 'pid,ppid,ruser,rgroup,args', 'ww', '--forest'])

	lines = []
	for line in output.splitlines():
		parts = line.split(None, 2)
		if len(parts) >= 2 and parts[1] == "2":
			continue
		lines.append(line)

	raw = {
		"Processes": "\n" + "\n".join(lines) + "\n"
	}

	return raw