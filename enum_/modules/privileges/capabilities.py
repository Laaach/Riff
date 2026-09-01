import subprocess

def capabilities():

    try:
        result = subprocess.run(["getcap", "-r", "/"], text=True, capture_output=True)
        content = result.stdout.strip() if result.returncode == 0 else "getcap failed"

    except FileNotFoundError:
        content = "getcap not installed"

    raw = {
        "Capabilities": content
    }

    return raw