#!/usr/bin/env python3
"""Login to Claude Code OAuth by piping in the login command and session token."""
import subprocess
import sys
import os
import time

claude_path = r'C:\Users\irfan\AppData\Local\hermes\node\claude'
oauth_code = 'kwjexXer4878QKaDn29iEzzPyUbnBU54aXoQsbFOKYsNqgU2#2jmTGdGm9naJvTiQezyyNqecs2ftbYDBb8YrKavXpe4'

# Method 1: Try echo pipe approach 
print("=== Method 1: Direct pipe ===")
proc = subprocess.Popen(
    [claude_path, '-p', '/login'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    cwd=os.path.expanduser('~'),
    env={**os.environ, 'CLAUDE_CODE': '1'}
)

# Send the OAuth code when prompted
time.sleep(5)
proc.stdin.write(oauth_code + '\n')
proc.stdin.flush()
time.sleep(3)

# Get any output
try:
    stdout, stderr = proc.communicate(timeout=20)
    print("STDOUT:", stdout[-500:] if stdout else "empty")
    if stderr:
        print("STDERR:", stderr[-200:])
    print("Exit code:", proc.returncode)
except subprocess.TimeoutExpired:
    proc.kill()
    print("Timeout")
