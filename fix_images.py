"""Fix broken product images by testing multiple candidate URLs and updating the DB."""
import urllib.request
import pymysql

# Multiple candidate photo IDs for each broken product (will try in order)
candidates = {
    3: ("Carrot", [
        "photo-1598170845058-32b9d6a5da37",
        "photo-1590868309235-ea34bed7bd7f",
        "photo-1445282768818-728615cc910a",
    ]),
    6: ("Potato", [
        "photo-1518977676601-b53f02ac6d5d",
        "photo-1590165482129-1b8b27698780",
        "photo-1596910547037-d56e1de4a7a0",
    ]),
    9: ("Mango", [
        "photo-1553279768-865429fa0078",
        "photo-1605027990121-cbae9e0642df",
        "photo-1591073113125-e46713c829ed",
    ]),
    10: ("Grapes", [
        "photo-1537640538966-79f369b41f8f",
        "photo-1596363505729-4190a9506133",
        "photo-1473090826765-d54ac2fdc1eb",
    ]),
    11: ("Pomegranate", [
        "photo-1615485925600-97237c4fc1ec",
        "photo-1541344999736-4d41311a0431",
        "photo-1579600161224-cac5a2971069",
    ]),
    12: ("Cauliflower", [
        "photo-1568584711075-3d021a7c3ce3",
        "photo-1613743983303-b3e89f8a2b80",
        "photo-1510627498534-cf7e9002facc",
    ]),
    13: ("Capsicum", [
        "photo-1563565186793-57e3afa7c4d3",
        "photo-1592841200221-a6898f367e86",
        "photo-1525607551316-4a25a8e2a68e",
    ]),
    14: ("Garlic", [
        "photo-1609205807990-9ec5fc9ee7b8",
        "photo-1540148426945-6cf22a6b2571",
        "photo-1501420193726-1f65acd36ac5",
    ]),
    20: ("Yogurt", [
        "photo-1488477181272-a9b4d21780cb",
        "photo-1584278858536-52532423b9ea",
        "photo-1557275357-072087771588",
    ]),
    24: ("Fresh Cream", [
        "photo-1563636619-e910ef2a844b",
        "photo-1587466280419-9a01cf867383",
        "photo-1563729784474-d77dbb933a9e",
    ]),
    31: ("Cola", [
        "photo-1624552184280-9e9811a2de91",
        "photo-1581636625402-29b2a704ef13",
        "photo-1629203851122-3726ecdf080e",
    ]),
    34: ("Soft Drink", [
        "photo-1530840928828-5ead79cabbf6",
        "photo-1581006852262-e4307cf6283a",
        "photo-1622708862399-78a4ab9e8f3e",
    ]),
    37: ("Biscuits", [
        "photo-1558961363-fa4f2323ef2c",
        "photo-1590080874088-efc49e70e7c8",
        "photo-1597733336794-12d05021d510",
    ]),
    41: ("Instant Noodles", [
        "photo-1612927335753-1573c004be51",
        "photo-1569718212165-3a8278d5f624",
        "photo-1555126634-323283e090fa",
    ]),
    43: ("Cashews", [
        "photo-1536591187872-b1903498ef4e",
        "photo-1509358271058-acd22cc93898",
        "photo-1563636619-e910ef2a844b",
    ]),
    44: ("Dates", [
        "photo-1559181567-c3190ca9be46",
        "photo-1584452101670-a0e976900e84",
        "photo-1610210840627-b1ab77af6f46",
    ]),
    45: ("Basmati Rice", [
        "photo-1586201327693-863a34a8e03e",
        "photo-1536304993881-c6e4e3f181e3",
        "photo-1594311431461-035cca46403b",
    ]),
    47: ("Moong Dal", [
        "photo-1612257998531-c0e2a0e37b7a",
        "photo-1585032226651-759b368d7246",
        "photo-1563729784474-d77dbb933a9e",
    ]),
    48: ("Chana Dal", [
        "photo-1609520778972-57c0a10bf03f",
        "photo-1585032226651-759b368d7246",
        "photo-1563729784474-d77dbb933a9e",
    ]),
    56: ("Salt", [
        "photo-1526459879085-136b9e7e5de7",
        "photo-1518113175641-fcda953930a6",
        "photo-1583394293214-28ded15ee548",
    ]),
    57: ("Cumin Seeds", [
        "photo-1599909631519-fb01bf00b2f2",
        "photo-1596040033229-a9821ebd058d",
        "photo-1563729784474-d77dbb933a9e",
    ]),
}

BASE = "https://images.unsplash.com/"
PARAMS = "?q=80&w=800&auto=format&fit=crop"

def test_url(photo_id):
    url = f"{BASE}{photo_id}{PARAMS}"
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.status == 200, url
    except:
        return False, url

conn = pymysql.connect(
    host='127.0.0.1', user='root', password='tiger',
    database='rasiii_db', cursorclass=pymysql.cursors.DictCursor
)
c = conn.cursor()

fixed = 0
still_broken = []

for pid, (name, photo_ids) in candidates.items():
    found = False
    for photo_id in photo_ids:
        ok, url = test_url(photo_id)
        if ok:
            c.execute("UPDATE products SET Image = %s WHERE ID = %s", (url, pid))
            print(f"  [FIXED] ID={pid} {name} -> {photo_id}")
            fixed += 1
            found = True
            break
    if not found:
        # Use a guaranteed fallback - generic grocery image
        fallback = f"{BASE}photo-1542838132-92c53300491e{PARAMS}"
        c.execute("UPDATE products SET Image = %s WHERE ID = %s", (fallback, pid))
        still_broken.append(name)
        print(f"  [FALLBACK] ID={pid} {name} -> generic grocery")

conn.commit()
conn.close()

print(f"\nFixed {fixed} images with specific photos.")
if still_broken:
    print(f"Used generic fallback for: {still_broken}")
print("Done!")
