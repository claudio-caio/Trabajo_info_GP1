import sqlite3, json, sys
from pathlib import Path
DB = Path(__file__).resolve().parents[1] / 'blog' / 'db.sqlite3'
if not DB.exists():
    print('DB not found:', DB)
    sys.exit(1)
conn = sqlite3.connect(str(DB))
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
rows = [r[0] for r in cur.fetchall()]
print(json.dumps(rows, indent=2))
conn.close()
