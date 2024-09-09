import sqlite3


conn = sqlite3.connect('instance/Quickr.db')
conn.execute('''
             CREATE TABLE users (
                 id INTEGER PRIMARY KEY,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL
                 first_name TEXT,
                 last_name TEXT
                 email TEXT UNIQUE NOT NULL
                 created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                 updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                 ''')
cursor = conn.cursor()

conn.commit()
cursor.close()
conn.close()