import subprocess


def run_command(command, input_text=None):
    try:
        result = subprocess.run(command,input=input_text,text=True, capture_output=True)
    except OSError as error:
        return f"{command[0]} unavailable: {error}"

    if result.returncode != 0:
        return result.stderr.strip() or f"{command[0]} failed (exit code {result.returncode})"

    return result.stdout.strip()