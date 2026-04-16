"""Update all product image URLs in the database with fresh, verified Unsplash URLs."""
import pymysql

photos = {
    "Apple": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?q=80&w=800&auto=format&fit=crop",
    "Banana": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?q=80&w=800&auto=format&fit=crop",
    "Carrot": "https://images.unsplash.com/photo-1647410766629-b851e34b9e2d?q=80&w=800&auto=format&fit=crop",
    "Tomato": "https://images.unsplash.com/photo-1546094096-0df4bcaaa337?q=80&w=800&auto=format&fit=crop",
    "Onion": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?q=80&w=800&auto=format&fit=crop",
    "Potato": "https://images.unsplash.com/photo-1632183993035-c2a50c27c68f?q=80&w=800&auto=format&fit=crop",
    "Spinach": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?q=80&w=800&auto=format&fit=crop",
    "Broccoli": "https://images.unsplash.com/photo-1615484477778-ca3b77940c25?q=80&w=800&auto=format&fit=crop",
    "Mango": "https://images.unsplash.com/photo-1601493700631-2851bdbb0b8b?q=80&w=800&auto=format&fit=crop",
    "Grapes": "https://images.unsplash.com/photo-1548584651-ac7f5e6e8b17?q=80&w=800&auto=format&fit=crop",
    "Pomegranate": "https://images.unsplash.com/photo-1633140498553-1a4a6ccf5f55?q=80&w=800&auto=format&fit=crop",
    "Cauliflower": "https://images.unsplash.com/photo-1568584711075-3d021a7c3ce3?q=80&w=800&auto=format&fit=crop",
    "Capsicum": "https://images.unsplash.com/photo-1563565186793-57e3afa7c4d3?q=80&w=800&auto=format&fit=crop",
    "Garlic": "https://images.unsplash.com/photo-1609205807990-9ec5fc9ee7b8?q=80&w=800&auto=format&fit=crop",
    "Ginger": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?q=80&w=800&auto=format&fit=crop",
    "Lemon": "https://images.unsplash.com/photo-1587486913049-53fc88980cfc?q=80&w=800&auto=format&fit=crop",
    "Milk": "https://images.unsplash.com/photo-1550583724-b2692b85b150?q=80&w=800&auto=format&fit=crop",
    "Cheese": "https://images.unsplash.com/photo-1618164435735-413d3b066c9a?q=80&w=800&auto=format&fit=crop",
    "Butter": "https://images.unsplash.com/photo-1601599561213-832382fd07ba?q=80&w=800&auto=format&fit=crop",
    "Yogurt": "https://images.unsplash.com/photo-1488477181272-a9b4d21780cb?q=80&w=800&auto=format&fit=crop",
    "Paneer": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?q=80&w=800&auto=format&fit=crop",
    "Ghee": "https://images.unsplash.com/photo-1558642891-54be180ea339?q=80&w=800&auto=format&fit=crop",
    "Curd": "https://images.unsplash.com/photo-1571212515416-fef01fc43637?q=80&w=800&auto=format&fit=crop",
    "Fresh Cream": "https://images.unsplash.com/photo-1563636619-e910ef2a844b?q=80&w=800&auto=format&fit=crop",
    "Buttermilk": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?q=80&w=800&auto=format&fit=crop",
    "Condensed Milk": "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?q=80&w=800&auto=format&fit=crop",
    "Tea Powder": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?q=80&w=800&auto=format&fit=crop",
    "Coffee Powder": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?q=80&w=800&auto=format&fit=crop",
    "Orange Juice": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?q=80&w=800&auto=format&fit=crop",
    "Apple Juice": "https://images.unsplash.com/photo-1576673442511-7e39b6545c87?q=80&w=800&auto=format&fit=crop",
    "Cola": "https://images.unsplash.com/photo-1624552184280-9e9811a2de91?q=80&w=800&auto=format&fit=crop",
    "Green Tea": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?q=80&w=800&auto=format&fit=crop",
    "Mineral Water": "https://images.unsplash.com/photo-1564419320461-6870880221ad?q=80&w=800&auto=format&fit=crop",
    "Soft Drink": "https://images.unsplash.com/photo-1530840928828-5ead79cabbf6?q=80&w=800&auto=format&fit=crop",
    "Energy Drink": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?q=80&w=800&auto=format&fit=crop",
    "Potato Chips": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?q=80&w=800&auto=format&fit=crop",
    "Biscuits": "https://images.unsplash.com/photo-1558961363-fa4f2323ef2c?q=80&w=800&auto=format&fit=crop",
    "Cookies": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?q=80&w=800&auto=format&fit=crop",
    "Namkeen": "https://images.unsplash.com/photo-1601050690597-df0568f70950?q=80&w=800&auto=format&fit=crop",
    "Popcorn": "https://images.unsplash.com/photo-1578849278619-e73505e9610f?q=80&w=800&auto=format&fit=crop",
    "Instant Noodles": "https://images.unsplash.com/photo-1612927335753-1573c004be51?q=80&w=800&auto=format&fit=crop",
    "Roasted Almonds": "https://images.unsplash.com/photo-1508817628294-5a453fa0b8fb?q=80&w=800&auto=format&fit=crop",
    "Cashews": "https://images.unsplash.com/photo-1536591187872-b1903498ef4e?q=80&w=800&auto=format&fit=crop",
    "Dates": "https://images.unsplash.com/photo-1559181567-c3190ca9be46?q=80&w=800&auto=format&fit=crop",
    "Basmati Rice": "https://images.unsplash.com/photo-1586201327693-863a34a8e03e?q=80&w=800&auto=format&fit=crop",
    "Toor Dal": "https://images.unsplash.com/photo-1582284540020-8acbe03f4924?q=80&w=800&auto=format&fit=crop",
    "Moong Dal": "https://images.unsplash.com/photo-1612257998531-c0e2a0e37b7a?q=80&w=800&auto=format&fit=crop",
    "Chana Dal": "https://images.unsplash.com/photo-1609520778972-57c0a10bf03f?q=80&w=800&auto=format&fit=crop",
    "Wheat Flour": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?q=80&w=800&auto=format&fit=crop",
    "Oats": "https://images.unsplash.com/photo-1614961233913-a5113a4a34ed?q=80&w=800&auto=format&fit=crop",
    "Sunflower Oil": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?q=80&w=800&auto=format&fit=crop",
    "Mustard Oil": "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?q=80&w=800&auto=format&fit=crop",
    "Turmeric Powder": "https://images.unsplash.com/photo-1615485499978-1279c3d6302f?q=80&w=800&auto=format&fit=crop",
    "Red Chilli Powder": "https://images.unsplash.com/photo-1585325701956-60dd9c8553bc?q=80&w=800&auto=format&fit=crop",
    "Garam Masala": "https://images.unsplash.com/photo-1532336414038-cf19250c5757?q=80&w=800&auto=format&fit=crop",
    "Salt": "https://images.unsplash.com/photo-1526459879085-136b9e7e5de7?q=80&w=800&auto=format&fit=crop",
    "Cumin Seeds": "https://images.unsplash.com/photo-1599909631519-fb01bf00b2f2?q=80&w=800&auto=format&fit=crop",
    "Black Pepper": "https://images.unsplash.com/photo-1599307767316-776533bb941c?q=80&w=800&auto=format&fit=crop",
    "Laundry Detergent": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?q=80&w=800&auto=format&fit=crop",
    "Dishwash Liquid": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=800&auto=format&fit=crop",
    "Floor Cleaner": "https://images.unsplash.com/photo-1563453392212-326f5e854473?q=80&w=800&auto=format&fit=crop",
    "Toilet Cleaner": "https://images.unsplash.com/photo-1585515320310-259814833e62?q=80&w=800&auto=format&fit=crop",
    "Bath Soap": "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?q=80&w=800&auto=format&fit=crop",
    "Shampoo": "https://images.unsplash.com/photo-1585751119414-ef2636f8aede?q=80&w=800&auto=format&fit=crop",
}

try:
    conn = pymysql.connect(
        host='127.0.0.1', user='root', password='tiger',
        database='rasiii_db', cursorclass=pymysql.cursors.DictCursor
    )
    c = conn.cursor()
    updated = 0
    not_found = []
    for name, url in photos.items():
        c.execute("UPDATE products SET Image = %s WHERE Name = %s", (url, name))
        if c.rowcount > 0:
            updated += 1
        else:
            not_found.append(name)
    conn.commit()
    conn.close()
    print(f"[OK] Updated {updated} product images successfully.")
    if not_found:
        print(f"[WARN] Not found in DB (skipped): {not_found}")
except Exception as e:
    print(f"[ERROR] {e}")
