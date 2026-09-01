from enum_.modules.privileges.shared.logic import filter_suid_sgid
from enum_.core.output.file_presenter import present

def sgid():
    _, sgids = filter_suid_sgid()

    return {
        "SGIDS": "\n".join(present(_sgid) for _sgid in sgids)
    }