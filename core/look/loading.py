import random
import time
import sys
from shared.look.colors import *

def loading(is_fast):
    loading_quotes = [
        'ＳＴＡＲＴＩＮＧ ＳＣＡＲＥ ＦＯＲＣＥ ＯＮＥ',
        'ＲＵＮＮＩＮＧ ＴＨＥ ＲＩＦＦ',
        'ＦＥＥＤＩＮＧ ＣＡＮＤＹ ＴＯ ＴＨＥ ＣＡＮＮＩＢＡＬ',
        'ＳＥＲＶＩＮＧ ＩＮ ＴＨＥ ＣＨＡＩＮＳＡＷ ＢＵＦＦＥＴ',
        'ＢＩＴＩＮＧ ＩＴ ＬＩＫＥ Ａ ＢＵＬＬＤＯＧ',
        'ＳＴＲＩＫＩＮＧ ＤＯＷＮ ＴＨＥ ＰＲＯＨＥＴＳ ＯＦ ＦＡＬＳＥ',
        'ＧＥＴＴＩＮＧ ＨＥＡＶＹ',
        'ＧＲＩＰ ＲＥＡＰＥＲ ＩＳ ＰＬＡＹＩＮＧ ＧＵＩＴＡＲ'
    ]

    loading_bar = random.choice(loading_quotes)

    delay = 0.01 if is_fast else 0.05

    target = random.randint(70, 95)
    for i in range(target // 2 + 1):
        sys.stdout.write(
            f"\r{DARK_GRAY}[{LIGHT_GRAY}{'█' * i}{DARK_GRAY}{'░' * (50 - i)}{BLACK}] {DARK_GRAY}{i * 2:3d}% {RED}{loading_bar}...{RESET}")
        sys.stdout.flush()
        time.sleep(delay)