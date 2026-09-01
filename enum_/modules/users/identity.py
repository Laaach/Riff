import os
from enum_.shared.utils import run_command


def identity():

	id_ = run_command(['id'])
	whoami = run_command(['whoami'])
	shell = os.getenv("SHELL") or "N/A"


	raw = {
		"ID": id_,
		"USER": whoami,
		"SHELL": shell
	}

	return raw