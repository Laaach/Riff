import sys

def module_output(name, iterated_lines, is_verbose, trim):

    if trim <= 0:
        sys.exit("Trim must be greater than 0")

    lines = []

    lines.append('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    lines.append(f'▓ 【 {name} 】')
    lines.append('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

    if is_verbose:
        visible_lines_amount = 99999999
    else:
        visible_lines_amount = trim

    for section, section_lines in iterated_lines.items():
        non_empty_lines = [line for line in section_lines if line.strip()]
        if not non_empty_lines:
            continue

        lines.append(f"  {section}")

        if len(non_empty_lines) <= 3 and all(len(line.strip()) <= 80 for line in non_empty_lines):
            for line in non_empty_lines:
                lines.append(f"   ▸ {line}")
        else:
            lines.append("  " + "─" * 60)

            visible_lines = non_empty_lines[:visible_lines_amount]

            for line in visible_lines:
                lines.append(f"  {line}")

            hidden = len(non_empty_lines) - len(visible_lines)

            if hidden > 0:
                lines.append(f"  ... {hidden} lines hidden.")

    return '\n'.join(lines)