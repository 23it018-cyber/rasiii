import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace pymysql with sqlite3
text = text.replace('import pymysql', 'import sqlite3')

# Replace get_db
db_setup = """def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn"""
text = re.sub(r'def get_db.*?return conn', db_setup, text, flags=re.DOTALL)

# Replace init_db
init_db_func = """def init_db():
    try:
        conn = get_db()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS products (
            ID INTEGER PRIMARY KEY,
            Category VARCHAR(255),
            Name VARCHAR(255),
            Price FLOAT,
            Stock INT,
            Image VARCHAR(255),
            Unit VARCHAR(50)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(255),
            Email VARCHAR(255),
            Password VARCHAR(255)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS orders (
            "Order ID" VARCHAR(255) PRIMARY KEY,
            "Customer Name" VARCHAR(255),
            Phone VARCHAR(255),
            Address TEXT,
            "Delivery Date" VARCHAR(255),
            Items TEXT,
            "Total Amount" FLOAT,
            Date VARCHAR(255),
            Time VARCHAR(255),
            Status VARCHAR(255)
        )''')
        
        c.execute("SELECT COUNT(*) as count FROM products")
        result = c.fetchone()
        if result and dict(result)['count'] == 0:
            print("Seeding SQLite with default products...")
            pid = 1
            price = 50
            for cat, items in GROCERY_PRODUCTS:
                for item, unit in items:
                    img = get_image_for_product(item, cat)
                    c.execute('''INSERT INTO products (ID, Category, Name, Price, Stock, Image, Unit)
                                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (pid, cat, item, price, 150, img, unit))
                    pid += 1
                    price = (price + 15) if price < 1500 else 50
            print("Seeded successfully!")
            
        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()"""
text = re.sub(r'def init_db\(\):.*?finally:.*?conn\.close\(\)', init_db_func, text, flags=re.DOTALL)

# Replace execute placeholders %s to ?
text = text.replace('WHERE ID = %s', 'WHERE ID = ?')
text = text.replace('VALUES (%s, %s, %s)', 'VALUES (?, ?, ?)')
text = text.replace('(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
text = text.replace('Stock = Stock - %s WHERE ID = %s', 'Stock = Stock - ? WHERE ID = ?')
text = text.replace('VALUES (%s, %s, %s, %s, %s, %s, %s)', 'VALUES (?, ?, ?, ?, ?, ?, ?)')
text = text.replace('Status = %s WHERE `Order ID` = %s', 'Status = ? WHERE "Order ID" = ?')

# Backticks to double quotes for SQLite
text = text.replace('`Order ID`', '"Order ID"')
text = text.replace('`Customer Name`', '"Customer Name"')
text = text.replace('`Delivery Date`', '"Delivery Date"')
text = text.replace('`Total Amount`', '"Total Amount"')

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Converted app.py to SQLite perfectly.")
