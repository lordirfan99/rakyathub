"""Patch ptai OpenAI provider to add User-Agent header."""
import sys

path = "/usr/local/lib/python3.13/dist-packages/engine/llm/providers/openai.py"

with open(path, "r") as f:
    content = f.read()

old = 'headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}'
new = 'headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}'

if old in content:
    content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)
    print("PATCHED: Added User-Agent header")
else:
    # Check if already patched
    if "User-Agent" in content:
        print("ALREADY PATCHED: User-Agent header exists")
    else:
        print("ERROR: Could not find the target line")
        print(f"Looking for: {old[:60]}...")
        sys.exit(1)

# Verify
with open(path, "r") as f:
    for i, line in enumerate(f, 1):
        if "headers" in line and "Authorization" in line:
            print(f"Line {i}: {line.rstrip()}")
