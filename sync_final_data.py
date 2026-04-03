import pymysql

def sync_final_prices():
    # Final exact data from the user request
    final_data = {
        "Apple": (50.0, "kg"),
        "Banana": (65.0, "kg"),
        "Carrot": (80.0, "kg"),
        "Tomato": (95.0, "kg"),
        "Onion": (110.0, "kg"),
        "Potato": (125.0, "kg"),
        "Spinach": (140.0, "pack"),
        "Broccoli": (155.0, "piece"),
        "Mango": (170.0, "kg"),
        "Grapes": (185.0, "kg"),
        "Pomegranate": (200.0, "kg"),
        "Cauliflower": (55.0, "piece"),
        "Capsicum": (70.0, "kg"),
        "Garlic": (85.0, "kg"),
        "Ginger": (100.0, "kg"),
        "Lemon": (15.0, "piece"),
        
        "Milk": (170.0, "litre"),
        "Cheese": (185.0, "pack"),
        "Butter": (200.0, "pack"),
        "Yogurt": (215.0, "pack"),
        "Paneer": (230.0, "pack"),
        "Ghee": (245.0, "litre"),
        "Curd": (45.0, "pack"),
        "Fresh Cream": (95.0, "pack"),
        "Buttermilk": (25.0, "litre"),
        "Condensed Milk": (80.0, "pack"),
        
        "Tea Powder": (260.0, "pack"),
        "Coffee Powder": (275.0, "pack"),
        "Orange Juice": (290.0, "litre"),
        "Apple Juice": (305.0, "litre"),
        "Cola": (320.0, "litre"),
        "Green Tea": (335.0, "pack"),
        "Mineral Water": (20.0, "litre"),
        "Soft Drink": (45.0, "litre"),
        "Energy Drink": (65.0, "pack"),
        
        "Potato Chips": (350.0, "pack"),
        "Biscuits": (365.0, "pack"),
        "Cookies": (380.0, "pack"),
        "Namkeen": (395.0, "pack"),
        "Popcorn": (410.0, "pack"),
        "Instant Noodles": (425.0, "pack"),
        "Roasted Almonds": (250.0, "pack"),
        "Cashews": (320.0, "pack"),
        "Dates": (180.0, "pack"),
        
        "Basmati Rice": (440.0, "kg"),
        "Toor Dal": (455.0, "kg"),
        "Moong Dal": (470.0, "kg"),
        "Chana Dal": (485.0, "kg"),
        "Wheat Flour": (500.0, "kg"),
        "Oats": (515.0, "pack"),
        
        "Sunflower Oil": (530.0, "litre"),
        "Mustard Oil": (545.0, "litre"),
        "Turmeric Powder": (560.0, "pack"),
        "Red Chilli Powder": (575.0, "pack"),
        "Garam Masala": (590.0, "pack"),
        "Salt": (605.0, "kg"),
        "Cumin Seeds": (120.0, "pack"),
        "Black Pepper": (145.0, "pack"),
        
        "Laundry Detergent": (620.0, "pack"),
        "Dishwash Liquid": (635.0, "litre"),
        "Floor Cleaner": (650.0, "litre"),
        "Toilet Cleaner": (665.0, "litre"),
        "Bath Soap": (680.0, "piece"),
        "Shampoo": (695.0, "piece")
    }

    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='tiger', database='rasiii_db')
        c = conn.cursor()
        print("Starting Final Price & Unit Precision Sync...")
        count = 0
        for name, (price, unit) in final_data.items():
            c.execute("UPDATE products SET Price = %s, Unit = %s WHERE Name = %s", (price, unit, name))
            count += c.rowcount
        conn.commit()
        conn.close()
        print(f"Sync Complete. Verified {count} products matches.")
    except Exception as e:
        print(f"Price Sync Error: {e}")

if __name__ == '__main__':
    sync_final_prices()
