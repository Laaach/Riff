from shared.look.colors import *

def _print_sections(matched_rules_data, is_color):

    _severity_colors = {
        "direct_root": BG_RED,
        "risky_config": RED,
        "flagged_secret": MAGENTA,
        "needs_review": YELLOW,
        "expected": CYAN
    }
    severity_colors = _severity_colors if is_color else {nothing: "" for nothing in _severity_colors}
    reset = RESET if is_color else ""

    sections = set()
    for finding in matched_rules_data:
        color = severity_colors[finding['Severity']]
        sections.add((
            f"\n────────────────────────────────────────────────────────────────"
            f"> {finding['ID']}\n"
            f"  Severity    : {color}{finding['Severity']}{reset}\n"
            f"  Description : {finding['Description']}\n"
            f"  Reference   : {finding['Reference']}\n"
            f"  Exploit     : {finding['Exploit']}"
        ))

    if not sections:
        sections.add("      ＮＯＴＨＩＮＧ ＨＥＲＥ ＢＵＴ ＤＯＮ＇Ｔ ＧＥＴ ＳＡＤ,\nＧＯ ＬＩＳＴＥＮ ＴＯ ＳＯＭＥ ＧＯＯＤ ＭＥＴＡＬ ＡＮＤ ＢＥ ＨＡＰＰＹ")

    return sections


def print_summary(matched_rules_data, is_color):

    print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print(f'██ 【 S U M M A R Y 】 ██')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    print('\n'.join(_print_sections(matched_rules_data, is_color)))

    print()

    print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('██ 【 E N D   O F   S U M M A R Y 】 ██')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')