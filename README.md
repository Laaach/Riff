# Riff

Riff is a Linux local privilege-escalation enumeration tool. It runs focused checks concurrently, matches results against local rules, and can display a condensed findings summary.

Use it only on systems you own or are explicitly authorized to assess.

## Requirements

- Python 3.8+
- Linux for the enumeration and process-monitor modes
- `inotify_simple` for the optional `pmon` mode

## Information
- Use the compiled version on the target system; do not use Python files.


```bash
python3 -m pip install inotify_simple
```

The enumeration and organizer modes otherwise use only the Python standard library and common Linux utilities. If a utility such as `ip`, `ss`, `ps`, or `sudo` is unavailable, Riff reports that in the corresponding module instead of terminating the scan.

## Run an enumeration scan

From the project directory:

```bash
python3 riff.py
```

Useful examples:

```bash
# Faster scan: omit SUID, SGID, and capability filesystem scans.
python3 riff.py --fast

# Run only named modules.
python3 riff.py --modules system network sudo --skip-loading

# Omit named modules from the normal scan.
python3 riff.py --exclude home processes

# Print only the findings summary.
python3 riff.py --silent --no-colors

# Save module output to a file.
python3 riff.py --output riff-output.txt
```

### Enumeration options

| Option | Description |
| --- | --- |
| `-m`, `--modules NAME [NAME ...]` | Run only the selected modules. |
| `-x`, `--exclude NAME [NAME ...]` | Exclude modules from the normal scan. |
| `-f`, `--fast` | Skip `suid`, `sgid`, and `capabilities`. |
| `-o`, `--output FILE` | Append module output to `FILE`. |
| `-v`, `--verbose` | Do not trim long module output. |
| `-s`, `--silent` | Suppress module output and show the summary. |
| `-t`, `--trim N` | Show at most `N` lines in long sections; default: `45`. |
| `-p`, `--password PASSWORD` | Supply a password to `sudo -lS` for `sudo`. |
| `--skip-loading` | Disable the loading animation. |
| `--summary` | Print the findings summary after module output. |
| `--list-modules` | Show the list of available modules. |
| `--no-colors` | Disable ANSI colour output. |

`--silent` and `--verbose` are incompatible.

### Module names

Use these exact names with `--modules` and `--exclude`:

| Module | Purpose |
| --- | --- |
| `system` | Host, kernel, architecture, and OS information. |
| `identity` | Current identity, username, and shell. |
| `network` | `/etc/hosts`, interfaces, and listening sockets. |
| `environment` | Environment variables. |
| `users` | Login-capable users and UID 0 accounts. |
| `sudo` | `sudo -lS` output when a password is supplied. |
| `etc` | Top-level world-readable or world-writable files in `/etc`. |
| `processes` | Process tree from `ps`. |
| `ssh` | Active SSH daemon configuration values. |
| `ftp` | Active vsftpd and ProFTPD configuration values. |
| `nfs` | `/etc/exports`, with a `showmount` fallback. |
| `cron` | System cron jobs and cron directories. |
| `home` | Home-directory SSH folders, history files, and private keys in `.ssh`. |
| `capabilities` | File capabilities from `getcap -r /`. |
| `suid` | Non-default SUID files. |
| `sgid` | Non-default SGID files. |
| `sessions` | Currently logged-in users. |
| `path` | Current user's `PATH` environment variable. |

## Process monitor

`pmon` observes filesystem activity with inotify and regularly scans `/proc` for new processes. It can still miss extremely short-lived processes.

```bash
python3 riff.py pmon
```

By default, `/tmp`, `/var`, `/home`, and `/opt` are watched recursively; `/usr` and `/etc` are watched non-recursively.

```bash
# Poll more frequently. Interval must be greater than zero.
python3 riff.py pmon --interval 0.02

# Add recursive and non-recursive watch paths.
python3 riff.py pmon --watch /srv/app --watch-flat /run

# Replace the default recursive paths.
python3 riff.py pmon --watch-only /tmp /srv/app
```

| Option | Description |
| --- | --- |
| `-I`, `--interval SECONDS` | Positive polling interval; default: `0.05`. |
| `-w`, `--watch PATH [PATH ...]` | Add recursively watched directories. |
| `--watch-flat PATH [PATH ...]` | Add non-recursively watched directories. |
| `--watch-only PATH [PATH ...]` | Replace the default recursive watch directories. |

Press `Ctrl-C` to stop monitoring.

## Organizer

The organizer reads and updates a JSON checklist selected through `RIFF_TEMPLATE_PATH`.

To preserve the bundled template, copy it before editing:

```bash
cp organizer/Templates/Template.json /tmp/riff-checklist.json
export RIFF_TEMPLATE_PATH=/tmp/riff-checklist.json
python3 riff.py org
```

```bash
# Update item 3.
python3 riff.py org --item 3 --status found --notes "Writable service script found"

# Add an item. Category and status are required.
python3 riff.py org --add --category "Services" --status unchecked --question "Review custom services"

# Remove item 3.
python3 riff.py org --remove --item 3
```

| Option | Description |
| --- | --- |
| `-i`, `--item N` | Select an item by its displayed index. |
| `-c`, `--category TEXT` | Set an item category. |
| `-q`, `--question TEXT` | Set an item question. |
| `-n`, `--notes TEXT` | Set item notes. |
| `-H`, `--hints TEXT` | Set command hints. |
| `-s`, `--status STATUS` | Set `found`, `not found`, or `unchecked`. |
| `-a`, `--add` | Add a checklist item. |
| `-r`, `--remove` | Remove the selected item. |

## Notes

- Results are local observations, not proof of exploitability. Validate each finding in the context of the target system and your authorization.
- Filesystem-wide capability, SUID, and SGID scans may take noticeably longer than other modules.
- The author is not responsible for any actions, changes, damage, or consequences resulting from the use or misuse of this tool. Use it only on systems you own or are explicitly authorized to assess.
