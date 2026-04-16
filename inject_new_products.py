import pymysql

def expand_inventory():
    new_products = [
        # Fruits & Vegetables
        ("Fruits & Vegetables", "Mango", "https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=800&auto=format&fit=crop", 170.0, "kg"),
        ("Fruits & Vegetables", "Grapes", "https://images.unsplash.com/photo-1537640538966-79f369b41f8f?q=80&w=800&auto=format&fit=crop", 185.0, "kg"),
        ("Fruits & Vegetables", "Pomegranate", "https://images.unsplash.com/photo-1615485925600-97237c4fc1ec?q=80&w=800&auto=format&fit=crop", 200.0, "kg"),
        ("Fruits & Vegetables", "Cauliflower", "https://images.unsplash.com/photo-1568584711075-3d021a7c3ce3?q=80&w=800&auto=format&fit=crop", 55.0, "piece"),
        ("Fruits & Vegetables", "Capsicum", "https://images.unsplash.com/photo-1563510330-84644f826ee2?q=80&w=800&auto=format&fit=crop", 70.0, "kg"),
        ("Fruits & Vegetables", "Garlic", "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=800&auto=format&fit=crop", 85.0, "kg"),
        ("Fruits & Vegetables", "Ginger", "https://images.unsplash.com/photo-1615850953584-932166a35f97?q=80&w=800&auto=format&fit=crop", 100.0, "kg"),
        ("Fruits & Vegetables", "Lemon", "https://images.unsplash.com/photo-1590505681916-aa55095e89a2?q=80&w=800&auto=format&fit=crop", 15.0, "piece"),
        
        # Dairy Products
        ("Dairy Products", "Curd", "https://images.unsplash.com/photo-1563208285-06264292e5db?q=80&w=800&auto=format&fit=crop", 45.0, "pack"),
        ("Dairy Products", "Fresh Cream", "https://images.unsplash.com/photo-1553909489-cd47e0907d3f?q=80&w=800&auto=format&fit=crop", 95.0, "pack"),
        ("Dairy Products", "Buttermilk", "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?q=80&w=800&auto=format&fit=crop", 25.0, "litre"),
        ("Dairy Products", "Condensed Milk", "https://images.unsplash.com/photo-1623157297962-d27376a91d24?q=80&w=800&auto=format&fit=crop", 80.0, "pack"),
        
        # Beverages
        ("Beverages", "Mineral Water", "https://images.unsplash.com/photo-1560023907-5ff24a0d9ef5?q=80&w=800&auto=format&fit=crop", 20.0, "litre"),
        ("Beverages", "Soft Drink", "https://images.unsplash.com/photo-1622483767028-3f66f344507c?q=80&w=800&auto=format&fit=crop", 45.0, "litre"),
        ("Beverages", "Energy Drink", "https://images.unsplash.com/photo-1632749610581-2e7ba10ae545?q=80&w=800&auto=format&fit=crop", 65.0, "pack"),
        
        # Snacks & Packaged Foods
        ("Snacks & Packaged Foods", "Roasted Almonds", "https://images.unsplash.com/photo-1508817628294-5a453fa0b8fb?q=80&w=800&auto=format&fit=crop", 250.0, "pack"),
        ("Snacks & Packaged Foods", "Cashews", "https://images.unsplash.com/photo-1615485238148-bf1846a21ad4?q=80&w=800&auto=format&fit=crop", 320.0, "pack"),
        ("Snacks & Packaged Foods", "Dates", "https://images.unsplash.com/photo-1626202133282-f831a279e722?q=80&w=800&auto=format&fit=crop", 180.0, "pack"),
        
        # Cooking Oils & Masala
        ("Cooking Oils & Masala", "Cumin Seeds", "https://images.unsplash.com/photo-1615485499978-1279c3d6302f?q=80&w=800&auto=format&fit=crop", 120.0, "pack"),
        ("Cooking Oils & Masala", "Black Pepper", "https://images.unsplash.com/photo-1599307767316-776533bb941c?q=80&w=800&auto=format&fit=crop", 145.0, "pack")
    ]

    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='tiger', database='rasiii_db')
        c = conn.cursor()
        
        # Get next ID
        c.execute("SELECT MAX(ID) FROM products")
        max_id = c.fetchone()[0] or 0
        next_id = max_id + 1
        
        print(f"Injecting 20 new products starting from ID {next_id}...")
        
        for cat, name, img, price, unit in new_products:
            c.execute('''INSERT INTO products (ID, Category, Name, Price, Stock, Image, Unit)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)''', (next_id, cat, name, price, 150, img, unit))
            next_id += 1
            
        conn.commit()
        conn.close()
        print("20 new products injected successfully.")
    except Exception as e:
        print(f"Injection error: {e}")

if __name__ == '__main__':
    expand_inventory()
