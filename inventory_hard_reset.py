import pymysql

def hard_reset_inventory():
    final_64_products = [
        # Category, Name, Unit, Price, ImageURL
        ("Fruits & Vegetables", "Apple", "kg", 50.0, "https://images.unsplash.com/photo-1560806887-1e4cd0b60205?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Banana", "kg", 65.0, "https://images.unsplash.com/photo-1603833665858-e61d17a86224?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Carrot", "kg", 80.0, "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Tomato", "kg", 95.0, "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Onion", "kg", 110.0, "https://images.unsplash.com/photo-1508747703725-719777637510?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Potato", "kg", 125.0, "https://images.unsplash.com/photo-1518977676601-b53f02ac6d5d?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Spinach", "pack", 140.0, "https://images.unsplash.com/photo-1576045057995-568f588f82fb?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Broccoli", "piece", 155.0, "https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Mango", "kg", 170.0, "https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Grapes", "kg", 185.0, "https://images.unsplash.com/photo-1537640538966-79f369b41f8f?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Pomegranate", "kg", 200.0, "https://images.unsplash.com/photo-1615485925600-97237c4fc1ec?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Cauliflower", "piece", 55.0, "https://images.unsplash.com/photo-1568584711075-3d021a7c3ce3?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Capsicum", "kg", 70.0, "https://images.unsplash.com/photo-1563510330-84644f826ee2?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Garlic", "kg", 85.0, "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Ginger", "kg", 100.0, "https://images.unsplash.com/photo-1615850953584-932166a35f97?q=80&w=800&auto=format&fit=crop"),
        ("Fruits & Vegetables", "Lemon", "piece", 15.0, "https://images.unsplash.com/photo-1590505681916-aa55095e89a2?q=80&w=800&auto=format&fit=crop"),

        ("Dairy Products", "Milk", "litre", 170.0, "https://images.unsplash.com/photo-1563636619-e910ef2a844b?q=80&w=800&auto=format&fit=crop"),
        ("Dairy Products", "Cheese", "pack", 185.0, "https://images.unsplash.com/photo-1486297678162-ad2a19b058f1?q=80&w=800&auto=format&fit=crop"),
        ("Dairy Products", "Butter", "pack", 200.0, "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?q=80&w=800&auto=format&fit=crop"),
        ("Dairy Products", "Yogurt", "pack", 215.0, "https://images.unsplash.com/photo-1584273143981-43c28586ed6a?q=80&w=800&auto=format&fit=crop"),
        ("Dairy Products", "Paneer", "pack", 230.0, "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?q=80&w=800&auto=format&fit=crop"),
        ("Dairy Products", "Ghee", "litre", 245.0, "https://images.unsplash.com/photo-1591125211993-e9912079c676?q=80&w=800&auto=format&fit=crop"),
        ("Dairy Products", "Curd", "pack", 45.0, "https://images.unsplash.com/photo-1563208285-06264292e5db?q=80&w=800&auto=format&fit=crop"),
        ("Dairy Products", "Fresh Cream", "pack", 95.0, "https://images.unsplash.com/photo-1553909489-cd47e0907d3f?q=80&w=800&auto=format&fit=crop"),
        ("Dairy Products", "Buttermilk", "litre", 25.0, "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?q=80&w=800&auto=format&fit=crop"),
        ("Dairy Products", "Condensed Milk", "pack", 80.0, "https://images.unsplash.com/photo-1623157297962-d27376a91d24?q=80&w=800&auto=format&fit=crop"),

        ("Beverages", "Tea Powder", "pack", 260.0, "https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?q=80&w=800&auto=format&fit=crop"),
        ("Beverages", "Coffee Powder", "pack", 275.0, "https://images.unsplash.com/photo-1559056191-723dfc092b37?q=80&w=800&auto=format&fit=crop"),
        ("Beverages", "Orange Juice", "litre", 290.0, "https://images.unsplash.com/photo-1600271886382-df5ff85acb41?q=80&w=800&auto=format&fit=crop"),
        ("Beverages", "Apple Juice", "litre", 305.0, "https://images.unsplash.com/photo-1568909340263-d38363a44cbe?q=80&w=800&auto=format&fit=crop"),
        ("Beverages", "Cola", "litre", 320.0, "https://images.unsplash.com/photo-1622483767028-3f66f344507c?q=80&w=800&auto=format&fit=crop"),
        ("Beverages", "Green Tea", "pack", 335.0, "https://images.unsplash.com/photo-1627435601361-ec25f5b1d0e5?q=80&w=800&auto=format&fit=crop"),
        ("Beverages", "Mineral Water", "litre", 20.0, "https://images.unsplash.com/photo-1560023907-5ff24a0d9ef5?q=80&w=800&auto=format&fit=crop"),
        ("Beverages", "Soft Drink", "litre", 45.0, "https://images.unsplash.com/photo-1622483767028-3f66f344507c?q=80&w=800&auto=format&fit=crop"),
        ("Beverages", "Energy Drink", "pack", 65.0, "https://images.unsplash.com/photo-1632749610581-2e7ba10ae545?q=80&w=800&auto=format&fit=crop"),

        ("Snacks & Packaged Foods", "Potato Chips", "pack", 350.0, "https://images.unsplash.com/photo-1566478989037-eec170784d0b?q=80&w=800&auto=format&fit=crop"),
        ("Snacks & Packaged Foods", "Biscuits", "pack", 365.0, "https://images.unsplash.com/photo-1603532648955-0393e01c8a54?q=80&w=800&auto=format&fit=crop"),
        ("Snacks & Packaged Foods", "Cookies", "pack", 380.0, "https://images.unsplash.com/photo-1558961363-fa4f2323ef2c?q=80&w=800&auto=format&fit=crop"),
        ("Snacks & Packaged Foods", "Namkeen", "pack", 395.0, "https://images.unsplash.com/photo-1601050690597-df0568f70950?q=80&w=800&auto=format&fit=crop"),
        ("Snacks & Packaged Foods", "Popcorn", "pack", 410.0, "https://images.unsplash.com/photo-1578849278619-e73505e9610f?q=80&w=800&auto=format&fit=crop"),
        ("Snacks & Packaged Foods", "Instant Noodles", "pack", 425.0, "https://images.unsplash.com/photo-1612927335753-1573c004be51?q=80&w=800&auto=format&fit=crop"),
        ("Snacks & Packaged Foods", "Roasted Almonds", "pack", 250.0, "https://images.unsplash.com/photo-1508817628294-5a453fa0b8fb?q=80&w=800&auto=format&fit=crop"),
        ("Snacks & Packaged Foods", "Cashews", "pack", 320.0, "https://images.unsplash.com/photo-1615485238148-bf1846a21ad4?q=80&w=800&auto=format&fit=crop"),
        ("Snacks & Packaged Foods", "Dates", "pack", 180.0, "https://images.unsplash.com/photo-1626202133282-f831a279e722?q=80&w=800&auto=format&fit=crop"),

        ("Rice, Dal & Grains", "Basmati Rice", "kg", 440.0, "https://images.unsplash.com/photo-1586201327693-863a34a8e03e?q=80&w=800&auto=format&fit=crop"),
        ("Rice, Dal & Grains", "Toor Dal", "kg", 455.0, "https://images.unsplash.com/photo-1518175005913-d0755796bb9d?q=80&w=800&auto=format&fit=crop"),
        ("Rice, Dal & Grains", "Moong Dal", "kg", 470.0, "https://images.unsplash.com/photo-1644318721752-9d3e527f6a7d?q=80&w=800&auto=format&fit=crop"),
        ("Rice, Dal & Grains", "Chana Dal", "kg", 485.0, "https://images.unsplash.com/photo-1631454593414-99859f71c162?q=80&w=800&auto=format&fit=crop"),
        ("Rice, Dal & Grains", "Wheat Flour", "kg", 500.0, "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=800&auto=format&fit=crop"),
        ("Rice, Dal & Grains", "Oats", "pack", 515.0, "https://images.unsplash.com/photo-1584263309413-ed9995077e61?q=80&w=800&auto=format&fit=crop"),

        ("Cooking Oils & Masala", "Sunflower Oil", "litre", 530.0, "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?q=80&w=800&auto=format&fit=crop"),
        ("Cooking Oils & Masala", "Mustard Oil", "litre", 545.0, "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?q=80&w=800&auto=format&fit=crop"),
        ("Cooking Oils & Masala", "Turmeric Powder", "pack", 560.0, "https://images.unsplash.com/photo-1615485499978-1279c3d6302f?q=80&w=800&auto=format&fit=crop"),
        ("Cooking Oils & Masala", "Red Chilli Powder", "pack", 575.0, "https://images.unsplash.com/photo-1532509176311-64d550c6bf0a?q=80&w=800&auto=format&fit=crop"),
        ("Cooking Oils & Masala", "Garam Masala", "pack", 590.0, "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?q=80&w=800&auto=format&fit=crop"),
        ("Cooking Oils & Masala", "Salt", "kg", 605.0, "https://images.unsplash.com/photo-1518113175641-fcda953930a6?q=80&w=800&auto=format&fit=crop"),
        ("Cooking Oils & Masala", "Cumin Seeds", "pack", 120.0, "https://images.unsplash.com/photo-1615485499978-1279c3d6302f?q=80&w=800&auto=format&fit=crop"),
        ("Cooking Oils & Masala", "Black Pepper", "pack", 145.0, "https://images.unsplash.com/photo-1599307767316-776533bb941c?q=80&w=800&auto=format&fit=crop"),

        ("Household Essentials", "Laundry Detergent", "pack", 620.0, "https://images.unsplash.com/photo-1584622781564-1d9876a13d00?q=80&w=800&auto=format&fit=crop"),
        ("Household Essentials", "Dishwash Liquid", "litre", 635.0, "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=800&auto=format&fit=crop"),
        ("Household Essentials", "Floor Cleaner", "litre", 650.0, "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=800&auto=format&fit=crop"),
        ("Household Essentials", "Toilet Cleaner", "litre", 665.0, "https://images.unsplash.com/photo-1584622781564-1d9876a13d00?q=80&w=800&auto=format&fit=crop"),
        ("Household Essentials", "Bath Soap", "piece", 680.0, "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?q=80&w=800&auto=format&fit=crop"),
        ("Household Essentials", "Shampoo", "piece", 695.0, "https://images.unsplash.com/photo-1559591931-ef84209c0586?q=80&w=800&auto=format&fit=crop"),
    ]

    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='tiger', database='rasiii_db')
        c = conn.cursor()
        
        print("Cleaning old inventory...")
        c.execute("DELETE FROM products")
        
        print(f"Injecting {len(final_64_products)} final products with precise data...")
        pid = 1
        for cat, name, unit, price, img in final_64_products:
            c.execute('''INSERT INTO products (ID, Category, Name, Price, Stock, Image, Unit)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)''', (pid, cat, name, price, 150, img, unit))
            pid += 1
            
        conn.commit()
        conn.close()
        print("Inventory Hard Reset Complete. All 64 items are now in the database with correct photos, prices, and units.")
    except Exception as e:
        print(f"Hard Reset Error: {e}")

if __name__ == '__main__':
    hard_reset_inventory()
