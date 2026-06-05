#!/usr/bin/env python3
"""Login to Claude Code via OAuth by piping through bash."""
import subprocess
import os
import time
import sys

oauth_code = 'kwjexXer4878QKaDn29iEzzPyUbnBU54aXoQsbFOKYsNqgU2#2jmTGdGm9naJvTiQezyyNqecs2ftbYDBb8YrKavXpe4'

# Method 2: Use bash to run claude
cmd = f'echo "{oauth_code}" | npx --yes claude -p "/login" 2>&1'
print(f"Running...")

proc = subprocess.Popen(
    ['bash', '-c', cmd],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    cwd=os.path.expanduser('~'),
    env={**os.environ}
)

try:
    stdout, stderr = proc.communicate(timeout=30)
    print("=== STDOUT ===")
    print(stdout[-2000:])
    if stderr:
        print("=== STDERR ===")
        print(stderr[-500:])
    print(f"\nExit: {proc.returncode}")
except subprocess.TimeoutExpired:
    proc.kill()
    print("Timeout after 30s")
