import re

# Fix homepage food items - replace emoji function
path = r'C:\Users\irfan\rakyathub\src\pages\index.astro'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Replace the emoji function with initial-letter function
old_fn = """function getEmoji(n) {
  const u = (n||'').toUpperCase();
  const EMOJI_MAP = { AYAM:'",chr(0x1F357),"' DAGING:'",chr(0x1F969),"' IKAN:'",chr(0x1F41F),"' TELUR:'",chr(0x1F95A),"' BERAS:'",chr(0x1F35A),"' MINYAK:'",chr(0x1FAD9),"' GULA:'",chr(0x1F9CA),"' TEPUNG:'",chr(0x1F33E),"' CILI:'",chr(0x1F336),"' BAWANG:'",chr(0x1F9C5),"' HALIA:'",chr(0x1FADA),"' KACANG:'",chr(0x1F95C),"' KUBIS:'",chr(0x1F96C),"' LOBAK:'",chr(0x1F955),"' TIMUN:'",chr(0x1F952),"' SANTAN:'",chr(0x1F965)," };
  for (const [k,v] of Object.entries(EMOJI_MAP)) if (u.includes(k)) return v;
  return '",chr(0x1F6D2),"';
}"""

# Actually, let me just do simple text replacements.
# The emoji function
c = c.replace(
    "function getEmoji(n) {",
    "function getInitial(n) {"
)
c = c.replace(
    "const EMOJI_MAP = { AYAM:'🍗', DAGING:'🥩', IKAN:'🐟', TELUR:'🥚', BERAS:'🍚', MINYAK:'🫙', GULA:'🧂', TEPUNG:'🌾', CILI:'🌶️', BAWANG:'🧅', HALIA:'🫚', KACANG:'🥜', KUBIS:'🥬', LOBAK:'🥕', TIMUN:'🥒', SANTAN:'🥥' };",
    ""
)
c = c.replace(
    "for (const [k,v] of Object.entries(EMOJI_MAP)) if (u.includes(k)) return v;",
    ""
)
c = c.replace(
    "return '🛒';",
    "return u.charAt(0) || '?';"
)

# 2. Replace {getEmoji(item.name||'')} with {getInitial(item.name||'')}
c = c.replace("getEmoji(item.name||'')", "getInitial(item.name||'')")

# 3. Replace emoji span with gradient letter badge
old_span = '<span class=\"text-lg sm:text-xl w-7 sm:w-8 text-center shrink-0\">{getInitial(item.name||\\'\\')}</span>'
c = c.replace(
    'getInitial(item.name||'')',
    "getInitial(item.name||'')"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!")
