import sqlite3
import shutil
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / 'blog' / 'db.sqlite3'
BACKUP = Path(__file__).resolve().parents[1] / 'blog' / 'db.sqlite3.backup_before_fix'

print('DB path:', DB)
print('Backup path:', BACKUP)

if not DB.exists():
    raise SystemExit('DB file not found: ' + str(DB))

shutil.copy2(DB, BACKUP)
print('Backup created.')

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Show current admin migration rows
print('Current django_migrations admin entries:')
for row in cur.execute("SELECT id, app, name FROM django_migrations WHERE app='admin'"):
    print(row)

# Delete admin migration rows
cur.execute("DELETE FROM django_migrations WHERE app='admin'")
conn.commit()
print('Deleted admin migration rows from django_migrations.')

# Show remaining admin rows
print('Remaining admin entries:')
for row in cur.execute("SELECT id, app, name FROM django_migrations WHERE app='admin'"):
    print(row)

conn.close()
print('Done')
