import sqlite3

def get_connection():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect('db/materials.db')

def fetch_raw_materials():
    """Fetch raw materials from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM raw_materials")
    materials = cursor.fetchall()
    conn.close()
    return materials

def save_product(product_name, materials):
    """Save product and associated raw materials to the database"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO products (name) VALUES (?)''', (product_name,))
    product_id = cursor.lastrowid

    for material_id, quantity in materials:
        cursor.execute('''INSERT INTO product_materials (product_id, material_id, quantity)
                          VALUES (?, ?, ?)''', (product_id, material_id, quantity))

    conn.commit()
    conn.close()
