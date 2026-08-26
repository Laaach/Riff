
def _normalize_line(line):
    line = line.lower().replace('=', ' ')
    parts = line.split(None, 1)

    if len(parts) != 2:
        return None

    key, value = parts
    return f"{key}: {value.strip()}"

def _read_config_file(config_file):
    try:
        with open(config_file, "r") as config_file:
            return config_file.readlines()
    except FileNotFoundError:
        return []


def _is_commented(line):
    return bool(line.startswith("#"))

def scan_config(config):

    try:
        lines = _read_config_file(config)
    except (FileNotFoundError, PermissionError):
        return ''

    active_lines = []
    for line in lines:
        line = line.strip()
        if _is_commented(line):
            continue

        normalized = _normalize_line(line)
        if normalized is None:
            continue

        active_lines.append(normalized)

    if active_lines:
        return "\n".join(active_lines)
    return ''