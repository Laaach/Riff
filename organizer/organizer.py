import json
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from shared.look.colors import *

def modify_template(template, item, category, question, notes, hints, status, remove, add):
    try:
        with open(template) as template_file:
            template_data = json.load(template_file)

        if item is not None:
            if not 1 <= item <= len(template_data["items"]):
                sys.exit("No item has this id")
            item_index = item - 1

        try:
            if remove and item is not None:
                template_data["items"].pop(item_index)

            elif add:
                template_data["items"].append({"category": category,"question": question,"hint": hints,"status": status,"note": notes})

            elif item is not None:
                selected_item = template_data["items"][item_index]

                if category is not None:
                    selected_item["category"] = category
                if question is not None:
                    selected_item["question"] = question
                if hints is not None:
                    selected_item["hint"] = hints
                if status is not None:
                    selected_item["status"] = status
                if notes is not None:
                    selected_item["note"] = notes

            with open(template, "w") as template_file:
                json.dump(template_data, template_file, indent=4)
        except IndexError:
            sys.exit("No item has this id")
    except PermissionError:
        sys.exit("Lack of permissions")
    except FileNotFoundError:
        sys.exit("File not found")
    except json.JSONDecodeError:
        sys.exit(f"Invalid JSON template: {template}")

def print_organizer(template):

    try:
        with open(template) as template_data:
            template_data = json.load(template_data)


        line_width = len(template_data['description']) + 25

        print()
        print(f"{MAGENTA}{template_data['name'].center(line_width)}{RESET}")
        print(f"{DARK_GRAY}{'=' * line_width}{RESET}")
        print(f"{DARK_GRAY}   Author: {RESET}{template_data['author']}")
        print(f"{DARK_GRAY}   Description: {RESET}{template_data['description']}")
        print(f"{DARK_GRAY}{'=' * line_width}{RESET}")
        print()

        status_colors = {
            "found": BG_RED,
            "not found": GREEN,
            "unchecked": DARK_GRAY,
        }

        block_number = 1
        target_column = line_width - 20

        for block in template_data["items"]:
            status = block["status"].lower()
            color = status_colors.get(status, RESET)

            prefix_plain = f"[{block_number}] {block['category']} "
            dash_count = max(1, target_column - len(prefix_plain))
            dashes = "─" * dash_count

            print(
                f"{CYAN}[{block_number}]{RESET} {block['category']} {dashes}──> [ {color}{status.upper()}{RESET} ]")
            print(f"  {DARK_GRAY}├─{RESET} {CYAN}Hints:{RESET} {block['hint']}")
            print(f"  {DARK_GRAY}└─{RESET} {CYAN}Notes:{RESET} {block['note']}")
            print()
            block_number += 1

    except PermissionError:
        sys.exit("Lack of permissions")
    except FileNotFoundError:
        sys.exit("File not found")
    except json.JSONDecodeError:
        sys.exit(f"Invalid JSON template: {template}")
