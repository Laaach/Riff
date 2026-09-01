import os

def environment():
    result = [f"{name}={value}" for name, value in os.environ.items()]

    raw = {
        "Environment": '\n'.join(result)
    }

    return raw
