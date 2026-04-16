import pymysql

def update_master_photos():
    # Curated High-Quality E-commerce Style Photos for all 64 products
    master_photos = {
        # Fruits & Vegetables
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

        # Dairy Products
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

        # Beverages
        "Tea Powder": "https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?q=80&w=800&auto=format&fit=crop",
        "Coffee Powder": "https://images.unsplash.com/photo-1559056191-723dfc092b37?q=80&w=800&auto=format&fit=crop",
        "Orange Juice": "https://images.unsplash.com/photo-1600271886382-df5ff85acb41?q=80&w=800&auto=format&fit=crop",
        "Apple Juice": "https://images.unsplash.com/photo-1568909340263-d38363a44cbe?q=80&w=800&auto=format&fit=crop",
        "Cola": "https://images.unsplash.com/photo-1622483767028-3f66f344507c?q=80&w=800&auto=format&fit=crop",
        "Green Tea": "https://images.unsplash.com/photo-1627435601361-ec25f5b1d0e5?q=80&w=800&auto=format&fit=crop",
        "Mineral Water": "https://images.unsplash.com/photo-1560023907-5ff24a0d9ef5?q=80&w=800&auto=format&fit=crop",
        "Soft Drink": "https://images.unsplash.com/photo-1622483767028-3f66f344507c?q=80&w=800&auto=format&fit=crop",
        "Energy Drink": "https://images.unsplash.com/photo-1632749610581-2e7ba10ae545?q=80&w=800&auto=format&fit=crop",

        # Snacks & Packaged Foods
        "Potato Chips": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?q=80&w=800&auto=format&fit=crop",
        "Biscuits": "https://images.unsplash.com/photo-1603532648955-0393e01c8a54?q=80&w=800&auto=format&fit=crop",
        "Cookies": "https://images.unsplash.com/photo-1558961363-fa4f2323ef2c?q=80&w=800&auto=format&fit=crop",
        "Namkeen": "https://images.unsplash.com/photo-1601050690597-df0568f70950?q=80&w=800&auto=format&fit=crop",
        "Popcorn": "https://images.unsplash.com/photo-1578849278619-e73505e9610f?q=80&w=800&auto=format&fit=crop",
        "Instant Noodles": "https://images.unsplash.com/photo-1612927335753-1573c004be51?q=80&w=800&auto=format&fit=crop",
        "Roasted Almonds": "https://images.unsplash.com/photo-1508817628294-5a453fa0b8fb?q=80&w=800&auto=format&fit=crop",
        "Cashews": "https://images.unsplash.com/photo-1615485238148-bf1846a21ad4?q=80&w=800&auto=format&fit=crop",
        "Dates": "https://images.unsplash.com/photo-1626202133282-f831a279e722?q=80&w=800&auto=format&fit=crop",

        # Rice, Dal & Grains
        "Basmati Rice": "https://images.unsplash.com/photo-1586201327693-863a34a8e03e?q=80&w=800&auto=format&fit=crop",
        "Toor Dal": "https://images.unsplash.com/photo-1518175005913-d0755796bb9d?q=80&w=800&auto=format&fit=crop",
        "Moong Dal": "https://images.unsplash.com/photo-1644318721752-9d3e527f6a7d?q=80&w=800&auto=format&fit=crop",
        "Chana Dal": "https://images.unsplash.com/photo-1631454593414-99859f71c162?q=80&w=800&auto=format&fit=crop",
        "Wheat Flour": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=800&auto=format&fit=crop",
        "Oats": "https://images.unsplash.com/photo-1584263309413-ed9995077e61?q=80&w=800&auto=format&fit=crop",

        # Cooking Oils & Masala
        "Sunflower Oil": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?q=80&w=800&auto=format&fit=crop",
        "Mustard Oil": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?q=80&w=800&auto=format&fit=crop",
        "Turmeric Powder": "https://images.unsplash.com/photo-1615485499978-1279c3d6302f?q=80&w=800&auto=format&fit=crop",
        "Red Chilli Powder": "https://images.unsplash.com/photo-1532509176311-64d550c6bf0a?q=80&w=800&auto=format&fit=crop",
        "Garam Masala": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?q=80&w=800&auto=format&fit=crop",
        "Salt": "https://images.unsplash.com/photo-1518113175641-fcda953930a6?q=80&w=800&auto=format&fit=crop",
        "Cumin Seeds": "https://images.unsplash.com/photo-1615485499978-1279c3d6302f?q=80&w=800&auto=format&fit=crop",
        "Black Pepper": "https://images.unsplash.com/photo-1599307767316-776533bb941c?q=80&w=800&auto=format&fit=crop",

        # Household Essentials
        "Laundry Detergent": "https://images.unsplash.com/photo-1584622781564-1d9876a13d00?q=80&w=800&auto=format&fit=crop",
        "Dishwash Liquid": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=800&auto=format&fit=crop",
        "Floor Cleaner": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=800&auto=format&fit=crop",
        "Toilet Cleaner": "https://images.unsplash.com/photo-1584622781564-1d9876a13d00?q=80&w=800&auto=format&fit=crop",
        "Bath Soap": "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?q=80&w=800&auto=format&fit=crop",
        "Shampoo": "https://images.unsplash.com/photo-1559591931-ef84209c0586?q=80&w=800&auto=format&fit=crop"
    }

    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='tiger', database='rasiii_db')
        c = conn.cursor()
        print("Starting Master Photo Consistency Sync...")
        count = 0
        for name, url in master_photos.items():
            c.execute("UPDATE products SET Image = %s WHERE Name = %s", (url, name))
            count += c.rowcount
        conn.commit()
        conn.close()
        print(f"Master Sync Complete. Verified and Updated {count} product images.")
    except Exception as e:
        print(f"Master Sync Error: {e}")

if __name__ == '__main__':
    update_master_photos()
