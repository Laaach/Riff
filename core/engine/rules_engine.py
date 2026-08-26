import json
import sys
import re
from pathlib import Path
from shared.look.colors import *

ROOT = Path(__file__).resolve().parents[2]

def _normalize_name_to_filename(module_name):
    return module_name.replace(' ', '_').lower() + '.json'

def get_rule_file(module_name):
    filename = _normalize_name_to_filename(module_name)
    return next(ROOT.rglob(filename))

def _normalize_raw_to_lines(raw):
    _lines = []
    for section, content in raw.items():
        for line in content.split('\n'):
            _lines.append(line)
    return _lines

def rules_engine(raw, module_name, is_color):

    lines = _normalize_raw_to_lines(raw)

    _severity_colors = {
        "direct_root": BG_RED,
        "risky_config": RED,
        "flagged_secret": MAGENTA,
        "needs_review": YELLOW,
        "expected": CYAN
    }

    severity_colors = _severity_colors if is_color else {nothing: "" for nothing in _severity_colors}
    reset = RESET if is_color else ""

    module_rule_file = get_rule_file(module_name)

    iterated_lines = {section: content.split('\n') for section, content in raw.items()}
    matched_rules_data = []

    with open(module_rule_file, 'r') as rules_file:
        rules_file = json.load(rules_file)

    for rule in rules_file["rules"]:

        rule_match = rule["match"]
        rule_id = rule["id"]
        rule_severity = rule["severity"]
        rule_description = rule["description"]
        rule_reference = rule["reference"]
        rule_exploit = rule["exploit"]

        if rule_match not in ["all", "any"]:
            continue
        for section, section_lines in iterated_lines.items():
            for i, line in enumerate(section_lines):
                results = []
                for rule_condition in rule["conditions"]:
                    if rule_condition["type"] == "regex":
                        results.append(bool(re.search(rule_condition["value"], line)))
                    else:
                        continue

                matched = all(results) if rule_match == "all" else any(results)

                if matched:
                    color = severity_colors[rule_severity]
                    section_lines[i] = f"{color}{line}{reset}"
                    matched_rules_data.append({
                        "ID": rule_id,
                        "Severity": rule_severity,
                        "Description": rule_description,
                        "Reference": rule_reference,
                        "Exploit": rule_exploit
                    })

    return iterated_lines, matched_rules_data