import os, glob

files = glob.glob('templates/*.html')
files.append('static/css/style.css')
replacements = {
    'MKS Premium Cracker Shop': 'Rasiii Mart',
    'Explosive Offers': 'Fresh Deals',
    'Festival Sale': 'Daily Essentials Sale',
    'Delivery Date': 'Preferred Delivery Slot',
    'Paid &amp; Processing': 'Order Placed',
    'Paid & Processing': 'Order Placed',
    'Premium Fancy Crackers': 'Groceries',
    'Crackers': 'Groceries',
    'Cracker': 'Grocery',
    'crackers': 'groceries',
    'cracker': 'grocery'
}

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    for old, new in replacements.items():
        content = content.replace(old, new)
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Done")
