"""Fix the remaining 4 products with fallback images."""
import urllib.request
import pymysql

# More candidates for the 4 remaining products
candidates = {
    13: ("Capsicum", [
        "photo-1563636619-e910ef2a844b",
        "photo-1596484552834-6a58f850e0a1",
        "photo-1518736114810-3f3bedfec66a",
        "photo-1594282486552-05b4d80fbb9f",
        "photo-1560964645-5296b5099677",
    ]),
    14: ("Garlic", [
        "photo-1587049332298-1c42e83937a7",
        "photo-1625229922690-7c2f0e048753",
        "photo-1596547609652-9cf5d8d76921",
        "photo-1501420193726-1f65acd36ac5",
        "photo-1559888292-e5f5c02b857a",
    ]),
    44: ("Dates", [
        "photo-1610210840627-b1ab77af6f46",
        "photo-1567306226416-28f0efdc88ce",
        "photo-1583185539970-2e7605e0ffa1", 
        "photo-1584452101670-a0e976900e84",
        "photo-1575218823251-f9d243b6f720",
    ]),
    45: ("Basmati Rice", [
        "photo-1536304993881-c6e4e3f181e3",
        "photo-1594311431461-035cca46403b",
        "photo-1555126634-323283e090fa",
        "photo-1516684732162-798a0062be99",
        "photo-1606471191009-63994c5f7309",
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

for pid, (name, photo_ids) in candidates.items():
    found = False
    for photo_id in photo_ids:
        ok, url = test_url(photo_id)
        if ok:
            c.execute("UPDATE products SET Image = %s WHERE ID = %s", (url, pid))
            print(f"  [FIXED] ID={pid} {name} -> {photo_id}")
            found = True
            break
        else:
            print(f"  [SKIP]  ID={pid} {name} -> {photo_id} (404)")
    if not found:
        print(f"  [STILL BROKEN] ID={pid} {name}")

conn.commit()
conn.close()
print("\nDone!")
