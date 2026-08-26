RESET = "\033[0m"

BLACK = "\033[0;30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
LIGHT_GRAY = "\033[38;5;254m" 
DARK_GRAY = "\033[90m"

BOLD_RED = "\033[1;31m"
BOLD_GREEN = "\033[1;32m"
BOLD_YELLOW = "\033[1;33m"
BOLD_BLUE = "\033[1;34m"
BOLD_MAGENTA = "\033[1;35m"
BOLD_CYAN = "\033[1;36m"
BOLD_WHITE = "\033[1;37m"

BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

ITALIC = "\033[2m"


def highlights(text,  is_not_color ,critical=None, warning=None, summary=None, info=None):
    critical = critical or []
    warning = warning or []
    info = info or []
    summary = summary or []

    if not is_not_color:
        for word in critical:
            text = text.replace(word, f"{BG_RED}{word}{RESET}")

        for word in warning:
            text = text.replace(word, f"{BOLD_YELLOW}{word}{RESET}")

        for word in info:
            text = text.replace(word, f"{CYAN}{word}{RESET}")

        for word in summary:
            text = text.replace(word, f"{ITALIC}{word}{RESET}")

    return text