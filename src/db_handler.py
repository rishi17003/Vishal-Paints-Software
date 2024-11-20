import sqlite3

def get_connection():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect('db/materials.db')

def setup_database():
    """Set up the database with necessary tables and sample data."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")


    # Create raw_materials table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS raw_materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        mat_type TEXT NOT NULL
    )
    ''')

    # Create raw_material_history table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS raw_material_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        raw_material_id INTEGER NOT NULL,
        change_type TEXT NOT NULL,  -- e.g., 'added', 'updated', 'deleted'
        old_price REAL,
        new_price REAL,
        change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (raw_material_id) REFERENCES raw_materials (id)
    )
    ''')

    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # Create product_materials table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        material_id INTEGER NOT NULL,
        quantity REAL NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id),
        FOREIGN KEY (material_id) REFERENCES raw_materials (id)
    )
    ''')

    # Insert sample data into raw_materials table
    materials = [
        ('P1', 227.00, 'Pigment'),
    ('P11', 109.00, 'Pigment'),
    ('P6', 170.00, 'Pigment'),
    ('P3', 560.00, 'Pigment'),
    ('P4', 158.00, 'Pigment'),
    ('P5', 109.00, 'Pigment'),
    ('P60', 59.00, 'Pigment'),
    ('P7', 115.00, 'Pigment'),
    ('P100', 35.00, 'Pigment'),
    ('P50', 125.00, 'Pigment'),
    ('P70', 130.00, 'Pigment'),
    ('Redoxide Powder', 15.00, 'Pigment'),
    ('White Whiting', 25.00, 'Pigment'),
    ('Talc', 104.00, 'Pigment'),
    ('A1', 162.00, 'Additive'),
    ('A2', 150.00, 'Additive'),
    ('HCO', 150.00, 'Additive'),
    ('ACE', 600.00, 'Additive'),
    ('PINCOIL', 150.00, 'Additive'),
    ('BRIGHT', 600.00, 'Additive'),
    ('CATALYST MATT', 225.00, 'Additive'),
    ('ICLAY', 308.00, 'Additive'),
    ('ICLAY JELLY 10%', 250.00, 'Additive'),
    ('LEAK 10%', 108.00, 'Additive'),
    ('OMEGA', 55.00, 'Additive'),
    ('DH', 134.00, 'Additive'),
    ('M1 50%', 125.00, 'Resin'),
    ('M1 70%', 124.00, 'Resin'),
    ('M6', 206.00, 'Resin'),
    ('Mo 70%', 220.00, 'Resin'),
    ('MD', 129.00, 'Resin'),
    ('MD 60%', 125.00, 'Resin'),
    ('R 920', 160.00, 'Resin'),
    ('DBTL', 40.00, 'Resin'),
    ('927', 109.00, 'Resin'),
    ('1030', 135.00, 'Resin'),
    ('S1', 100.00, 'Thinner'),
    ('C1', 1.00, 'Thinner'),
    ('S6', 128.50, 'Thinner'),
    ('S20', 47.50, 'Thinner'),
    ('BA (Kg)', 135.00, 'Thinner'),
    ('BA (Lit)', 116.50, 'Thinner'),
    ('ETHYLE', 230.00, 'Thinner'),
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO raw_materials (name, price, mat_type) 
    VALUES (?, ?, ?)
    ''', materials)

    conn.commit()
    conn.close()



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
        

def update_raw_material_price(material_id, new_price):
    """
    Update the price of a raw material and log the change in history.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT price FROM raw_materials WHERE id = ?", (material_id,))
    old_price = cursor.fetchone()

    if old_price:
        old_price = old_price[0]

        if old_price != new_price:
            cursor.execute("UPDATE raw_materials SET price = ? WHERE id = ?", (new_price, material_id))

            cursor.execute("""
                INSERT INTO raw_material_history (material_id, change_type, old_price, new_price)
                VALUES (?, 'updated', ?, ?)
            """, (material_id, old_price, new_price))
            
            conn.commit()

    conn.close()

def fetch_raw_material_history():
    """
    Fetch raw material history records from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT h.id, r.name, h.old_price, h.new_price, h.change_date
        FROM raw_material_history h
        JOIN raw_materials r ON h.material_id = r.id
        ORDER BY h.change_date DESC
    """)
    history = cursor.fetchall()

    conn.close()
    return history

def delete_raw_material(material_id):
    """
    Delete a raw material and log the deletion in history.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, price FROM raw_materials WHERE id = ?", (material_id,))
    material = cursor.fetchone()

    if material:
        name, old_price = material

        cursor.execute("""
            INSERT INTO raw_material_history (material_id, change_type, old_price, new_price)
            VALUES (?, 'deleted', ?, NULL)
        """, (material_id, old_price))

        cursor.execute("DELETE FROM raw_materials WHERE id = ?", (material_id,))
        conn.commit()

    conn.close()



    conn.commit()
    conn.close()
