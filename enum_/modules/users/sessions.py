import subprocess

def sessions():
    try:
        result = subprocess.run(['who'], text=True, capture_output=True)
        content = result.stdout.strip() if result.returncode == 0 else "who failed or permission denied"
    except FileNotFoundError:
        content = "who not installed"

    raw = {
        "Logged Users": content
    }

    return raw

