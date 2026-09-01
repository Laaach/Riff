from enum_.modules.privileges.shared.logic import filter_suid_sgid
from enum_.core.output.file_presenter import present


def suid():
	suids, _ = filter_suid_sgid()

	return {
		"SUIDS": "\n".join(present(_suid) for _suid in suids)
	}



