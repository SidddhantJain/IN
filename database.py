import sqlite3

DB_NAME = "inventory.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            purchased_qty INTEGER NOT NULL,
            received_qty INTEGER NOT NULL,
            client_orders INTEGER NOT NULL,
            dispatched_qty INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_item(model, purchased_qty, received_qty, client_orders, dispatched_qty):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO inventory (model, purchased_qty, received_qty, client_orders, dispatched_qty)
        VALUES (?, ?, ?, ?, ?)
    ''', (model, purchased_qty, received_qty, client_orders, dispatched_qty))
    conn.commit()
    conn.close()

def get_inventory():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    data = c.fetchall()
    conn.close()
    return data

def update_item(item_id, model, purchased_qty, received_qty, client_orders, dispatched_qty):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE inventory
        SET model = ?, purchased_qty = ?, received_qty = ?, client_orders = ?, dispatched_qty = ?
        WHERE id = ?
    ''', (model, purchased_qty, received_qty, client_orders, dispatched_qty, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
