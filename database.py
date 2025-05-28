import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect("inventory.db", check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        purchased_qty INTEGER,
        received_qty INTEGER,
        client_orders INTEGER,
        dispatched_qty INTEGER
    )''')
    conn.commit()

def add_item(model, purchased_qty, received_qty, client_orders, dispatched_qty):
    c.execute('''INSERT INTO inventory (model, purchased_qty, received_qty, client_orders, dispatched_qty)
                 VALUES (?, ?, ?, ?, ?)''',
              (model, purchased_qty, received_qty, client_orders, dispatched_qty))
    conn.commit()

def get_inventory():
    c.execute("SELECT * FROM inventory")
    return c.fetchall()

def update_item(id, model, purchased_qty, received_qty, client_orders, dispatched_qty):
    c.execute('''UPDATE inventory SET model=?, purchased_qty=?, received_qty=?, client_orders=?, dispatched_qty=?
                 WHERE id=?''',
              (model, purchased_qty, received_qty, client_orders, dispatched_qty, id))
    conn.commit()

def delete_item(id):
    c.execute("DELETE FROM inventory WHERE id=?", (id,))
    conn.commit()
