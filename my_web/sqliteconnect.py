import sqlite3

conn = sqlite3.connect("eflyer.db")

c = conn.cursor()

c.execute('''
   CREATE TABLE IF NOT EXISTS registration (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL,
        address TEXT,
        gender TEXT ,
        dob DATE,
        phone_no TEXT ,
        email TEXT  NOT NULL,
        country TEXT,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
