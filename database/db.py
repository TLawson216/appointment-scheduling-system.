import sqlite3

def init_db():
    
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

#User table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
        )
    ''')
    
    cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
    user = cursor.fetchone()

    if not user:
        cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "1234")
    )

#appointment table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT,
            description TEXT,
            business_id INTEGER,
            status TEXT,
            cancel_reason TEXT
        )
    ''')

    conn.commit()
    conn.close()