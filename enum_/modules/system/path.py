import os

def path():

    path = os.getenv("PATH") or "N/A"

    raw = {
        "PATH": path
    }

    return raw
