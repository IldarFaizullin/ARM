import sqlite3

def init_db():
    conn = sqlite3.connect("appdata.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def add_order(name, price):
    conn = sqlite3.connect("appdata.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()

def get_orders():
    conn = sqlite3.connect("appdata.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM orders")
    rows = cursor.fetchall()
    conn.close()
    return rows