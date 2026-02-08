"""Sync buildozer.spec requirements from top-level requirements.txt.

This script extracts package names from `requirements.txt`, filters them
against a small whitelist of packages commonly required on mobile (Kivy,
plyer, etc.), and writes a comma-separated `requirements = python3,...`
line into `buildozer.spec`.

Run this after editing `requirements.txt` to keep `buildozer.spec` in sync:

    python scripts/sync_buildozer_requirements.py

Note: Buildozer requires the `requirements` field to be a comma-separated
list. This script makes a best-effort selection; review `buildozer.spec`
before building.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REQ_FILE = ROOT / 'requirements.txt'
BUILD_FILE = ROOT / 'buildozer.spec'

# Whitelist of packages that make sense to include in an Android build.
# Add more known mobile-friendly packages here if needed.
MOBILE_WHITELIST = {
    'kivy',
    'plyer',
    'pyjnius',
    'requests',
    'cryptography',
}


def parse_req_line(line: str):
    # Strip inline comments and whitespace
    line = re.sub(r"#.*$", "", line).strip()
    if not line:
        return None
    # Split on version specifiers (==, >=, <=, ~=, >, <)
    name = re.split(r"[=<>!~]+", line)[0].strip()
    # Extras (package[extra]) -> package
    name = re.split(r"\[", name)[0].strip()
    return name.lower() if name else None


def main():
    if not REQ_FILE.exists():
        print(f"requirements.txt not found at {REQ_FILE}")
        return 1
    pkg_names = []
    for ln in REQ_FILE.read_text().splitlines():
        nm = parse_req_line(ln)
        if nm:
            pkg_names.append(nm)

    mobile_pkgs = [p for p in pkg_names if p in MOBILE_WHITELIST]
    # Always include python3 for buildozer
    final = ['python3'] + mobile_pkgs

    if not BUILD_FILE.exists():
        print(f"buildozer.spec not found at {BUILD_FILE}")
        return 1

    text = BUILD_FILE.read_text()
    # Replace the requirements line (simple approach)
    new_req_line = 'requirements = ' + ','.join(final)
    new_text = re.sub(r'^requirements\s*=.*$', new_req_line, text, flags=re.MULTILINE)

    if new_text == text:
        # If no match, append the requirements under [app]
        new_text = text + '\n' + new_req_line + '\n'

    BUILD_FILE.write_text(new_text)
    print(f"Updated buildozer.spec requirements: {','.join(final)}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
