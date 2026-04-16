import pymysql

def fix_broken_photos():
    # Final 25 verified working IDs
    fix_mapping = {
        "Apple": "photo-1623815242959-fb20354f9b8d",
        "Potato": "photo-1518977676601-b53f02ac6d5d",
        "Grapes": "photo-1633033983258-8343a24eb102",
        "Cauliflower": "photo-1566842600175-97dca489844f",
        "Capsicum": "photo-1632992468155-a1ff2ca70f68",
        "Ginger": "photo-1544400127-ec33742f5348",
        "Lemon": "photo-1590736704728-f4730bb3c3db",
        "Milk": "photo-1576186726115-4d51596775d1",
        "Cheese": "photo-1762698978443-95bd7aa7afae",
        "Yogurt": "photo-1511690656952-34342bb7c2f2",
        "Ghee": "FhXM0LQoaEU",
        "Curd": "s5iMLdARRLI",
        "Fresh Cream": "Zo_AXwyCb4M",
        "Condensed Milk": "Y5sv2BhuJ70",
        "Coffee Powder": "YZERIZj6ZgY",
        "Orange Juice": "cxrG5kW0qX8",
        "Apple Juice": "AbzVoVX6DHU",
        "Cola": "L7ugLVFdejY",
        "Mineral Water": "3SDC8b1D-xI",
        "Biscuits": "C9RiYpk4bFI",
        "Cookies": "5YG2ZZgpJM0",
        "Basmati Rice": "xhs6vuE5oLY",
        "Toor Dal": "TUf3H3vRlNU",
        "Moong Dal": "7KgWPxA4eog",
        "Chana Dal": "vX_8u3Lp8Q0"
    }

    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='tiger', database='rasiii_db')
        c = conn.cursor()
        print("Starting Precision Photo Fix for 25 failing items...")
        count = 0
        for name, photo_id in fix_mapping.items():
            url = f"https://images.unsplash.com/{photo_id}?q=80&w=800&auto=format&fit=crop"
            c.execute("UPDATE products SET Image = %s WHERE Name = %s", (url, name))
            count += c.rowcount
            
        conn.commit()
        conn.close()
        print(f"Fix Complete. Successfully updated {count} broken photos with verified stable links.")
    except Exception as e:
        print(f"Fix Error: {e}")

if __name__ == '__main__':
    fix_broken_photos()
