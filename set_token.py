import re

env_path = 'C:/Users/irfan/AppData/Local/hermes/.env'
token = 'kwjexXer4878QKaDn29iEzzPyUbnBU54aXoQsbFOKYsNqgU2#2jmTGdGm9naJvTiQezyyNqecs2ftbYDBb8YrKavXpe4'

with open(env_path, 'r') as f:
    content = f.read()

# Replace ANTHROPIC_TOKEN line
new_content = re.sub(
    r'^ANTHROPIC_TOKEN=.*$',
    f'ANTHROPIC_TOKEN={token}',
    content,
    flags=re.MULTILINE
)

with open(env_path, 'w') as f:
    f.write(new_content)

print("ANTHROPIC_TOKEN set successfully")
print(f"Length: {len(token)}")

# Verify
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('ANTHROPIC_TOKEN='):
            val = line.split('=', 1)[1].strip()
            print(f"Verify: starts with {val[:10]}... length {len(val)}")
