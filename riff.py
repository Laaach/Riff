import concurrent.futures
import os
import sys
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
from core.engine.cli import module_choice
from core.engine.runner.registry import registry
from core.engine.runner.dispatch import dispatch
from shared.output.summary import print_summary
from core.look.banner import print_banner
from organizer.organizer import print_organizer, modify_template
from shared.look.colors import *

try:
	from pmon.pmon import pmon
	pmon_imported = True
except ImportError:
	pmon_imported = False

print_banner()

mode , args = module_choice()

try:
	is_color = not args.no_colors
except AttributeError:
	is_color = False

try:
	if mode == "enum":

		if args.silent:
			args.summary = True

		modules_to_run = registry(args.fast, args.modules, args.exclude, args.skip_loading, args.default, args.password)


		def run_module(module_name, function):
			try:
				return module_name, function(), None
			except Exception as _error:
				return module_name, None, _error


		with concurrent.futures.ThreadPoolExecutor() as executor:
			futures = [executor.submit(run_module, module_name, function)
				for module_name, function in modules_to_run.items()
			]
			results = [future.result() for future in futures]

			if not args.skip_loading:
				sys.stdout.write(f"\r{DARK_GRAY}[{LIGHT_GRAY}{'█' * 50}{DARK_GRAY}] "f"{DARK_GRAY}100%{RESET}\n")

		matched_rules_data = []
		for module_name, raw, error in results:
			if module_name == "loading":
				continue
			if error is not None:
				print(f"[!] {module_name} failed: {type(error).__name__}: {error}", file=sys.stderr)
				continue
			try:
				matched_rules_data.extend(dispatch(module_name, args.output, is_color, raw,args.verbose, args.silent, args.trim))
			except Exception as error:
				print(f"[!] {module_name} output/rules failed: "f"{type(error).__name__}: {error}", file=sys.stderr)



		if args.summary:
			print_summary(matched_rules_data, is_color)

	elif mode == "org":
		template_path = os.environ.get("RIFF_TEMPLATE_PATH")

		if template_path:
			template = template_path
		else:
			sys.exit("Please set RIFF_TEMPLATE_PATH if you want to use organizer")

		if args.remove and args.item is None:
			sys.exit("--remove requires --item")

		if (
				args.category or args.question or args.notes or args.hints or args.status) and args.item is None and not args.add:
			sys.exit("Editing requires --item")

		if args.add and not (args.category and args.status):
			sys.exit("--add requires --category and --status")

		if args.item is not None or args.add or args.remove:
			modify_template(template, args.item, args.category, args.question, args.notes, args.hints, args.status, args.remove, args.add)

		print_organizer(template)
	elif mode == "pmon":
		if not pmon_imported:
			sys.exit("pmon requires inotify_simple. Install it with: python3 -m pip install inotify_simple")

		if args.watch_only:
			recursive_dirs = args.watch_only
		else:
			recursive_dirs = ["/tmp", "/var", "/home", "/opt"] + (args.watch or [])

		flat_dirs = ["/usr", "/etc"] + (args.watch_flat or [])

		pmon(args.interval, recursive_dirs , flat_dirs)


except KeyboardInterrupt:
	print("\n")