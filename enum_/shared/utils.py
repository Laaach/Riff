import subprocess


def run_command(command, input_text=None):
    try:
        result = subprocess.run(command,input=input_text,text=True, capture_output=True)
    except OSError as error:
        return f"{command[0]} unavailable: {error}"

    if result.returncode != 0:
        return result.stderr.strip() or f"{command[0]} failed (exit code {result.returncode})"

    return result.stdout.strip()

def remove_comments_and_blanks(lines):
    active_lines = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        active_lines.append(line)

    return active_lines