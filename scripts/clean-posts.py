#!/usr/bin/env python3
"""
Proper YAML-aware sanitization. Uses PyYAML to parse frontmatter,
clean the excerpt field, and rewrite without corrupting structure.
"""
import os, re, glob
import yaml

POST_DIR = "C:/Users/irfan/rakyathub/src/data/post"

def sanitize_excerpt(text):
    if not text:
        return text
    # Remove raw image URLs in parens
    text = re.sub(r'\(https?://[^\s)]+\)', '', text)
    # Remove bare wp-content URLs
    text = re.sub(r'https?://[^\s]*wp-content[^\s]*', '', text, flags=re.IGNORECASE)
    # Remove <figure> and <figcaption> (complete and partial)
    text = re.sub(r'<figure[^>]*>[\s\S]*?</figure>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<figure\b[^>\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<figcaption\b[^>\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?figcaption[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?figure[^>]*>', '', text, flags=re.IGNORECASE)
    # Remove caption attributes
    text = re.sub(r"caption\s+id\s*=\s*['\"]attachment_\d+['\"][^)]*", '', text, flags=re.IGNORECASE)
    # Remove WordPress shortcodes
    text = re.sub(r'\[caption[^\]]*\][\s\S]*?\[/caption\]', '', text, flags=re.IGNORECASE)
    # Clean whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = [l.strip() for l in text.split('\n')]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    result = '\n'.join(lines)
    return result if result else None

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into frontmatter + body
    if not content.startswith('---\n'):
        return False
    
    end = content.find('\n---\n', 4)
    if end == -1:
        return False
    
    fm_text = content[4:end]
    body = content[end+5:]
    
    # Parse frontmatter with YAML
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        print(f"  YAML PARSE ERROR in {os.path.basename(filepath)}")
        return False
    
    if not fm or 'excerpt' not in fm:
        return False
    
    original_excerpt = fm['excerpt']
    cleaned = sanitize_excerpt(original_excerpt)
    
    if cleaned == original_excerpt:
        return False
    
    # Also clean body shortcodes
    body = re.sub(r'\\\[caption[^\]]*\\\][\s\S]*?\\\[/caption\\\]', '', body, flags=re.IGNORECASE)
    body = re.sub(r'\[caption[^\]]*\]', '', body, flags=re.IGNORECASE)
    body = re.sub(r'\[/caption\]', '', body, flags=re.IGNORECASE)
    # Clean body figure/figcaption tags
    body = re.sub(r'<figure[^>]*>[\s\S]*?</figure>', '', body, flags=re.IGNORECASE)
    body = re.sub(r'<figure\b[^>\n]*', '', body, flags=re.IGNORECASE)
    body = re.sub(r'<figcaption\b[^>\n]*', '', body, flags=re.IGNORECASE)
    body = re.sub(r'</?figcaption[^>]*>', '', body, flags=re.IGNORECASE)
    body = re.sub(r'</?figure[^>]*>', '', body, flags=re.IGNORECASE)
    
    # Update excerpt
    fm['excerpt'] = cleaned
    
    # Rebuild frontmatter preserving order
    # Use yaml.dump with proper formatting
    new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False, width=200)
    new_content = '---\n' + new_fm + '---\n' + body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

files = sorted(glob.glob(os.path.join(POST_DIR, '*.md')))
print(f"Processing {len(files)} post files...")
changed = 0
for fp in files:
    fname = os.path.basename(fp)
    try:
        if clean_file(fp):
            changed += 1
            print(f"  CLEANED: {fname}")
        else:
            print(f"  SKIP: {fname}")
    except Exception as e:
        import traceback
        print(f"  ERROR: {fname}: {e}")
        traceback.print_exc()
print(f"Done. {changed}/{len(files)} files cleaned.")
