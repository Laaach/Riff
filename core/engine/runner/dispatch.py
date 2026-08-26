from core.engine.rules_engine import rules_engine
from enum_.core.output.module_output import module_output
import sys

def dispatch(module_name, output_file, is_color, raw, is_verbose, is_silent, trim):

    iterated_lines, matched_rules_data = rules_engine(raw, module_name , is_color)

    if output_file:
        try:
            with open(output_file, 'a', encoding='UTF-8') as output_file:
                output_file.write(module_output(module_name, iterated_lines, is_verbose, trim))
        except PermissionError:
            sys.exit("Lack of permissions.")
    else:
        if not is_silent:
            print(module_output(module_name, iterated_lines, is_verbose, trim))
        else:
            pass

    return matched_rules_data