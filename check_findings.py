"""Extract finding details from ptai findings database."""
import sqlite3
import json

conn = sqlite3.connect("/root/.local/share/pentest-ai/findings.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# List tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cur.fetchall()]
print(f"Tables: {tables}")

for name in tables:
    cur.execute(f"PRAGMA table_info({name})")
    cols = cur.fetchall()
    
    cur.execute(f"SELECT COUNT(*) FROM {name}")
    count = cur.fetchone()[0]
    print(f"\n{'='*60}")
    print(f"TABLE: {name}")
    print(f"Columns: {len(cols)}, Rows: {count}")
    
    if count > 0:
        # Get column names
        col_names = [c[1] for c in cols]
        
        # Check if there's an engagement_id column
        if 'engagement_id' in col_names:
            # Show by engagement
            cur.execute(f"SELECT engagement_id, COUNT(*) as cnt FROM {name} GROUP BY engagement_id ORDER BY cnt DESC")
            eng_counts = cur.fetchall()
            for ec in eng_counts:
                print(f"  Engagement {ec[0]}: {ec[1]} findings")
        
        # Show all findings with key details
        cur.execute(f"SELECT * FROM {name} LIMIT 100")
        rows = cur.fetchall()
        for r in rows:
            row_dict = dict(r)
            # Print key fields
            title = row_dict.get('title', 'N/A')
            severity = row_dict.get('severity', row_dict.get('criticality', 'N/A'))
            target = str(row_dict.get('target_url', row_dict.get('target', 'N/A')))[:80]
            desc = str(row_dict.get('description', row_dict.get('detail', 'N/A')))[:300]
            print(f"\n  [{severity}] {title}")
            print(f"  Target: {target}")
            if desc and desc != 'N/A':
                print(f"  Detail: {desc}")
conn.close()
