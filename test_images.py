"""Test all product image URLs and report which ones are broken."""
import urllib.request
import pymysql

conn = pymysql.connect(
    host='127.0.0.1', user='root', password='tiger',
    database='rasiii_db', cursorclass=pymysql.cursors.DictCursor
)
c = conn.cursor()
c.execute("SELECT ID, Name, Image FROM products ORDER BY ID")
products = c.fetchall()
conn.close()

broken = []
working = []

for p in products:
    name = p['Name']
    url = p['Image']
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        resp = urllib.request.urlopen(req, timeout=10)
        if resp.status == 200:
            working.append(name)
        else:
            broken.append((p['ID'], name, resp.status))
    except Exception as e:
        broken.append((p['ID'], name, str(e)))

print(f"Working: {len(working)}/{len(products)}")
print(f"Broken: {len(broken)}/{len(products)}")
if broken:
    print("\nBroken products:")
    for pid, name, err in broken:
        print(f"  ID={pid} {name}: {err}")
