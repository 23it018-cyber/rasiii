import pymysql
from datetime import datetime

# Seeding Data - Final 64 Product Master List (Unique Photos)
GROCERY_PRODUCTS = [
    ("Fruits & Vegetables", [
        ("Apple", "kg"), ("Banana", "kg"), ("Carrot", "kg"), ("Tomato", "kg"), 
        ("Onion", "kg"), ("Potato", "kg"), ("Spinach", "pack"), ("Broccoli", "piece"),
        ("Mango", "kg"), ("Grapes", "kg"), ("Pomegranate", "kg"), ("Cauliflower", "piece"),
        ("Capsicum", "kg"), ("Garlic", "kg"), ("Ginger", "kg"), ("Lemon", "piece")
    ]),
    ("Dairy Products", [
        ("Milk", "litre"), ("Cheese", "pack"), ("Butter", "pack"), ("Yogurt", "pack"),
        ("Paneer", "pack"), ("Ghee", "litre"), ("Curd", "pack"), ("Fresh Cream", "pack"),
        ("Buttermilk", "litre"), ("Condensed Milk", "pack")
    ]),
    ("Beverages", [
        ("Tea Powder", "pack"), ("Coffee Powder", "pack"), ("Orange Juice", "litre"),
        ("Apple Juice", "litre"), ("Cola", "litre"), ("Green Tea", "pack"),
        ("Mineral Water", "litre"), ("Soft Drink", "litre"), ("Energy Drink", "pack")
    ]),
    ("Snacks & Packaged Foods", [
        ("Potato Chips", "pack"), ("Biscuits", "pack"), ("Cookies", "pack"),
        ("Namkeen", "pack"), ("Popcorn", "pack"), ("Instant Noodles", "pack"),
        ("Roasted Almonds", "pack"), ("Cashews", "pack"), ("Dates", "pack")
    ]),
    ("Rice, Dal & Grains", [
        ("Basmati Rice", "kg"), ("Toor Dal", "kg"), ("Moong Dal", "kg"),
        ("Chana Dal", "kg"), ("Wheat Flour", "kg"), ("Oats", "pack")
    ]),
    ("Cooking Oils & Masala", [
        ("Sunflower Oil", "litre"), ("Mustard Oil", "litre"), ("Turmeric Powder", "pack"),
        ("Red Chilli Powder", "pack"), ("Garam Masala", "pack"), ("Salt", "kg"),
        ("Cumin Seeds", "pack"), ("Black Pepper", "pack")
    ]),
    ("Household Essentials", [
        ("Laundry Detergent", "pack"), ("Dishwash Liquid", "litre"), ("Floor Cleaner", "litre"),
        ("Toilet Cleaner", "litre"), ("Bath Soap", "piece"), ("Shampoo", "piece")
    ])
]

# Helper to map UNIQUE photos during seed
def get_photo_url(name):
    photos = {
        "Apple": "https://images.unsplash.com/photo-1560806887-1e4cd0b60205?q=80&w=800&auto=format&fit=crop",
        "Banana": "https://images.unsplash.com/photo-1603833665858-e61d17a86224?q=80&w=800&auto=format&fit=crop",
        "Carrot": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?q=80&w=800&auto=format&fit=crop",
        "Tomato": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?q=80&w=800&auto=format&fit=crop",
        "Onion": "https://images.unsplash.com/photo-1508747703725-719777637510?q=80&w=800&auto=format&fit=crop",
        "Potato": "https://images.unsplash.com/photo-1518977676601-b53f02ac6d5d?q=80&w=800&auto=format&fit=crop",
        "Spinach": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?q=80&w=800&auto=format&fit=crop",
        "Broccoli": "https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?q=80&w=800&auto=format&fit=crop",
        "Mango": "https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=800&auto=format&fit=crop",
        "Grapes": "https://images.unsplash.com/photo-1537640538966-79f369b41f8f?q=80&w=800&auto=format&fit=crop",
        "Pomegranate": "https://images.unsplash.com/photo-1615485925600-97237c4fc1ec?q=80&w=800&auto=format&fit=crop",
        "Cauliflower": "https://images.unsplash.com/photo-1568584711075-3d021a7c3ce3?q=80&w=800&auto=format&fit=crop",
        "Capsicum": "https://images.unsplash.com/photo-1563510330-84644f826ee2?q=80&w=800&auto=format&fit=crop",
        "Garlic": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=800&auto=format&fit=crop",
        "Ginger": "https://images.unsplash.com/photo-1615850953584-932166a35f97?q=80&w=800&auto=format&fit=crop",
        "Lemon": "https://images.unsplash.com/photo-1590505681916-aa55095e89a2?q=80&w=800&auto=format&fit=crop",
        "Milk": "https://images.unsplash.com/photo-1563636619-e910ef2a844b?q=80&w=800&auto=format&fit=crop",
        "Cheese": "https://images.unsplash.com/photo-1486297678162-ad2a19b058f1?q=80&w=800&auto=format&fit=crop",
        "Butter": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?q=80&w=800&auto=format&fit=crop",
        "Yogurt": "https://images.unsplash.com/photo-1584273143981-43c28586ed6a?q=80&w=800&auto=format&fit=crop",
        "Paneer": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?q=80&w=800&auto=format&fit=crop",
        "Ghee": "https://images.unsplash.com/photo-1591125211993-e9912079c676?q=80&w=800&auto=format&fit=crop",
        "Curd": "https://images.unsplash.com/photo-1563208285-06264292e5db?q=80&w=800&auto=format&fit=crop",
        "Fresh Cream": "https://images.unsplash.com/photo-1553909489-cd47e0907d3f?q=80&w=800&auto=format&fit=crop",
        "Buttermilk": "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?q=80&w=800&auto=format&fit=crop",
        "Condensed Milk": "https://images.unsplash.com/photo-1623157297962-d27376a91d24?q=80&w=800&auto=format&fit=crop",
        "Tea Powder": "https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?q=80&w=800&auto=format&fit=crop",
        "Coffee Powder": "https://images.unsplash.com/photo-1559056191-723dfc092b37?q=80&w=800&auto=format&fit=crop",
        "Orange Juice": "https://images.unsplash.com/photo-1600271886382-df5ff85acb41?q=80&w=800&auto=format&fit=crop",
        "Apple Juice": "https://images.unsplash.com/photo-1568909340263-d38363a44cbe?q=80&w=800&auto=format&fit=crop",
        "Cola": "https://images.unsplash.com/photo-1622483767028-3f66f344507c?q=80&w=800&auto=format&fit=crop",
        "Green Tea": "https://images.unsplash.com/photo-1627435601361-ec25f5b1d0e5?q=80&w=800&auto=format&fit=crop",
        "Mineral Water": "https://images.unsplash.com/photo-1560023907-5ff24a0d9ef5?q=80&w=800&auto=format&fit=crop",
        "Soft Drink": "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?q=80&w=800&auto=format&fit=crop",
        "Energy Drink": "https://images.unsplash.com/photo-1632749610581-2e7ba10ae545?q=80&w=800&auto=format&fit=crop",
        "Potato Chips": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?q=80&w=800&auto=format&fit=crop",
        "Biscuits": "https://images.unsplash.com/photo-1603532648955-0393e01c8a54?q=80&w=800&auto=format&fit=crop",
        "Cookies": "https://images.unsplash.com/photo-1558961363-fa4f2323ef2c?q=80&w=800&auto=format&fit=crop",
        "Namkeen": "https://images.unsplash.com/photo-1601050690597-df0568f70950?q=80&w=800&auto=format&fit=crop",
        "Popcorn": "https://images.unsplash.com/photo-1578849278619-e73505e9610f?q=80&w=800&auto=format&fit=crop",
        "Instant Noodles": "https://images.unsplash.com/photo-1612927335753-1573c004be51?q=80&w=800&auto=format&fit=crop",
        "Roasted Almonds": "https://images.unsplash.com/photo-1508817628294-5a453fa0b8fb?q=80&w=800&auto=format&fit=crop",
        "Cashews": "https://images.unsplash.com/photo-1615485238148-bf1846a21ad4?q=80&w=800&auto=format&fit=crop",
        "Dates": "https://images.unsplash.com/photo-1626202133282-f831a279e722?q=80&w=800&auto=format&fit=crop",
        "Basmati Rice": "https://images.unsplash.com/photo-1586201327693-863a34a8e03e?q=80&w=800&auto=format&fit=crop",
        "Toor Dal": "https://images.unsplash.com/photo-1518175005913-d0755796bb9d?q=80&w=800&auto=format&fit=crop",
        "Moong Dal": "https://images.unsplash.com/photo-1644318721752-9d3e527f6a7d?q=80&w=800&auto=format&fit=crop",
        "Chana Dal": "https://images.unsplash.com/photo-1631454593414-99859f71c162?q=80&w=800&auto=format&fit=crop",
        "Wheat Flour": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=800&auto=format&fit=crop",
        "Oats": "https://images.unsplash.com/photo-1584263309413-ed9995077e61?q=80&w=800&auto=format&fit=crop",
        "Sunflower Oil": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?q=80&w=800&auto=format&fit=crop",
        "Mustard Oil": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?q=80&w=800&auto=format&fit=crop",
        "Turmeric Powder": "https://images.unsplash.com/photo-1615485499978-1279c3d6302f?q=80&w=800&auto=format&fit=crop",
        "Red Chilli Powder": "https://images.unsplash.com/photo-1532509176311-64d550c6bf0a?q=80&w=800&auto=format&fit=crop",
        "Garam Masala": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?q=80&w=800&auto=format&fit=crop",
        "Salt": "https://images.unsplash.com/photo-1518113175641-fcda953930a6?q=80&w=800&auto=format&fit=crop",
        "Cumin Seeds": "https://images.unsplash.com/photo-1632733711679-5292d6899f81?q=80&w=800&auto=format&fit=crop",
        "Black Pepper": "https://images.unsplash.com/photo-1599307767316-776533bb941c?q=80&w=800&auto=format&fit=crop",
        "Laundry Detergent": "https://images.unsplash.com/photo-1584622781564-1d9876a13d00?q=80&w=800&auto=format&fit=crop",
        "Dishwash Liquid": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=800&auto=format&fit=crop",
        "Floor Cleaner": "https://images.unsplash.com/photo-1563453392212-326f5e854473?q=80&w=800&auto=format&fit=crop",
        "Toilet Cleaner": "https://images.unsplash.com/photo-1549449852-51c6c6460060?q=80&w=800&auto=format&fit=crop",
        "Bath Soap": "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?q=80&w=800&auto=format&fit=crop",
        "Shampoo": "https://images.unsplash.com/photo-1559591931-ef84209c0586?q=80&w=800&auto=format&fit=crop"
    }
    return photos.get(name, "https://via.placeholder.com/800")

# ─── DATABASE SETUP ──────────────────────────────────────────────────────────

def get_db():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='tiger',
        database='rasiii_db',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def init_db():
    try:
        conn = get_db()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS products (
            ID INT PRIMARY KEY,
            Category VARCHAR(255),
            Name VARCHAR(255),
            Price FLOAT,
            Stock INT,
            Image VARCHAR(255),
            Unit VARCHAR(50)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(255),
            Email VARCHAR(255),
            Password VARCHAR(255)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS orders (
            `Order ID` VARCHAR(255) PRIMARY KEY,
            `Customer Name` VARCHAR(255),
            Phone VARCHAR(255),
            Address TEXT,
            `Delivery Date` VARCHAR(255),
            Items TEXT,
            `Total Amount` FLOAT,
            Date VARCHAR(255),
            Time VARCHAR(255),
            Status VARCHAR(255)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            message TEXT,
            date VARCHAR(255)
        )''')
        
        c.execute("SELECT COUNT(*) as count FROM products")
        result = c.fetchone()
        if result and result['count'] == 0:
            print("Seeding MySQL with UNIQUE Rasiii target collection...")
            pid = 1
            # Exact prices logic
            prices = [50, 65, 80, 95, 110, 125, 140, 155, 170, 185, 200, 55, 70, 85, 100, 15,
                      170, 185, 200, 215, 230, 245, 45, 95, 25, 80,
                      260, 275, 290, 305, 320, 335, 20, 45, 65,
                      350, 365, 380, 395, 410, 425, 250, 320, 180,
                      440, 455, 470, 485, 500, 515,
                      530, 545, 560, 575, 590, 605, 120, 145,
                      620, 635, 650, 665, 680, 695]
            
            p_idx = 0
            for cat, items in GROCERY_PRODUCTS:
                for item, unit in items:
                    price = prices[p_idx] if p_idx < len(prices) else 50
                    img = get_photo_url(item)
                    c.execute('''INSERT INTO products (ID, Category, Name, Price, Stock, Image, Unit)
                                 VALUES (%s, %s, %s, %s, %s, %s, %s)''', (pid, cat, item, price, 150, img, unit))
                    pid += 1
                    p_idx += 1
            print("Success: Final 64 UNIQUE collection synced to source.")
            
        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

# ─── DB HELPER FUNCTIONS ─────────────────────────────────────────────────────

def get_products():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(e)
        return []

def get_product_by_id(pid):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE ID = %s", (int(pid),))
        row = c.fetchone()
        conn.close()
        return row
    except:
        return None

def get_users():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        conn.close()
        return rows
    except:
        return []

def add_user(user_data):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO users (Username, Email, Password) VALUES (%s, %s, %s)", 
                  (user_data.get('Username'), user_data.get('Email'), user_data.get('Password')))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def add_contact_message(name, email, message):
    try:
        conn = get_db()
        c = conn.cursor()
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO contact_messages (name, email, message, date) VALUES (%s, %s, %s, %s)", (name, email, message, date))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Contact Error: {e}")

def get_contact_messages():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM contact_messages ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return []

def get_orders():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT `Order ID`, `Customer Name`, Phone, Address, `Delivery Date`, Items, `Total Amount`, Date, Time, Status FROM orders')
        rows = c.fetchall()
        conn.close()
        return rows
    except:
        return []

def add_order(order_data):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''INSERT INTO orders (`Order ID`, `Customer Name`, Phone, Address, `Delivery Date`, Items, `Total Amount`, Date, Time, Status)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                  (order_data.get('Order ID'), order_data.get('Customer Name'), order_data.get('Phone'),
                   order_data.get('Address'), order_data.get('Delivery Date'), order_data.get('Items'),
                   order_data.get('Total Amount'), order_data.get('Date'), order_data.get('Time'), order_data.get('Status')))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def update_stock(cart):
    try:
        conn = get_db()
        c = conn.cursor()
        for pid_str, item in cart.items():
            qty = item['quantity']
            c.execute("UPDATE products SET Stock = Stock - %s WHERE ID = %s", (qty, int(pid_str)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to update stock: {e}")

def get_max_product_id():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT MAX(ID) as max_id FROM products")
        row = c.fetchone()
        conn.close()
        return row['max_id'] if (row and row['max_id'] is not None) else 0
    except:
        return 0

def add_product_direct(pid, category, name, price, stock, image, unit):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''INSERT INTO products (ID, Category, Name, Price, Stock, Image, Unit)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)''', (pid, category, name, price, stock, image, unit))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error adding product: {e}")

def delete_product_direct(pid):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE ID = %s", (int(pid),))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error deleting product: {e}")
        
def update_order_status_direct(order_id, status):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('UPDATE orders SET Status = %s WHERE `Order ID` = %s', (status, order_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error updating order status: {e}")
