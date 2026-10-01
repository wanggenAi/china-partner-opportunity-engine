"""Fail closed if private paths or known contact values enter tracked files."""
from pathlib import Path
import os
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
tracked = subprocess.check_output(["git", "ls-files"], cwd=root, text=True).splitlines()
blocked = ("private/", ".env", "local_profile.json", "secrets/")
bad_paths = [p for p in tracked if p == ".env" or p.startswith(blocked)]
if bad_paths:
    print("Private paths are tracked:", *bad_paths, sep="\n")
    raise SystemExit(1)

contacts = tuple(
    value.strip().strip("\"'")
    for line in (root / ".env.local").read_text(encoding="utf-8").splitlines()
    if "=" in line and (value := line.split("=", 1)[1].strip())
) if (root / ".env.local").exists() else ()
patterns = [re.compile(r"(?<!\d)1\d{10}(?!\d)")]
hits = []
for name in tracked:
    path = root / name
    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for value in contacts + tuple(p.pattern for p in patterns):
            if value.startswith("(?"):
                if patterns[0].search(text):
                    hits.append(f"{name}: private phone-shaped value")
                continue
            if value in text:
                hits.append(f"{name}: {value}")
if hits:
    print("Private contact values found:", *hits, sep="\n")
    raise SystemExit(1)
print(f"Public scan passed ({len(tracked)} tracked files).")
