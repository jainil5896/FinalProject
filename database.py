import sqlite3

def create_db():
    conn = sqlite3.connect('tax_payments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_date TEXT,
            status TEXT,
            due_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()