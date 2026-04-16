with open('app.py', 'r', encoding='utf-8') as f:
    t = f.read()

t = t.replace('return rows', 'return [dict(r) for r in rows]')
t = t.replace('return row', 'return dict(row) if row else None')
t = t.replace("['Premium Fancy Crackers', 'Fancy Sky Shots']", "['Fruits & Vegetables', 'Household Essentials', 'Dairy Products']")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(t)
