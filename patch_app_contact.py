with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if "c.execute(\"SELECT COUNT(*) as count FROM products\")" in line:
        # Inject CREATE TABLE for contact prior to seeding logic
        new_lines.append("""        c.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            email VARCHAR(255),
            message TEXT,
            date VARCHAR(255)
        )''')\n""")
        new_lines.append(line)
    elif "def get_orders():" in line:
        # Inject DB helpers for contacts right above get_orders
        new_lines.append("""def add_contact_message(name, email, message):
    try:
        from datetime import datetime
        conn = get_db()
        c = conn.cursor()
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO contact_messages (name, email, message, date) VALUES (?, ?, ?, ?)", (name, email, message, date))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Contact Error: {e}")

def get_contact_messages():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM contact_messages ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        return []\n\n""")
        new_lines.append(line)
    elif "def contact():" in line:
        # Re-write contact route
        new_lines.append("""@app.route('/contact', methods=['GET', 'POST'])
def contact():
    location = "Rasiii Mart HQ, Organic Farm Distribution Center, Tamil Nadu, India"
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        add_contact_message(name, email, message)
        flash("Thank you! Your message has been safely received. Our support team will reach out shortly.", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html', location=location)
""")
    elif "@app.route('/contact')" in line:
        pass # Handle deleting the old decorator
    elif "location =" in line and "def contact():" not in "".join(lines[max(0, i-5):i]): 
        # Don't keep the old location= inside the old contact() if our manual rewrite is handling it.
        # It's better to just skip old contact body precisely.
        pass 
    elif "return render_template('contact.html', location=location)" in line and "def contact():" not in "".join(lines[max(0, i-5):i]):
        pass
    else:
        new_lines.append(line)

# Let me refine the contact route replacement safely by finding its index block
def patch_contact_route(content_lines):
    out = []
    skip = False
    for line in content_lines:
        if line.startswith("@app.route('/contact')"):
            skip = True
            out.append("""@app.route('/contact', methods=['GET', 'POST'])
def contact():
    location = "Rasiii Mart HQ, Organic Farm Distribution Center, Tamil Nadu, India"
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        add_contact_message(name, email, message)
        flash("Thank you! Your message has been safely received. Our support team will reach out shortly.", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html', location=location)\n""")
            continue
        if skip and line.strip() == "":
            skip = False
            out.append(line)
            continue
        if skip:
            continue
        out.append(line)
    return out

# Fix admin dashboard
def patch_admin_dashboard(content_lines):
    out = []
    for line in content_lines:
        if "products = get_products()" in line:
            out.append(line)
            out.append("    contacts = get_contact_messages()\n")
        elif "total_sales=total_sales)" in line:
            out.append(line.replace("total_sales=total_sales)", "total_sales=total_sales,\n                           contacts=contacts)"))
        else:
            out.append(line)
    return out

with open('app.py', 'r', encoding='utf-8') as f:
    text_lines = f.readlines()

text_lines = patch_contact_route(text_lines)
text_lines = patch_admin_dashboard(text_lines)

# Also apply the first loops (init_db, and helpers)
new_lines = []
for line in text_lines:
    if "c.execute(\"SELECT COUNT(*) as count FROM products\")" in line:
        new_lines.append("""        c.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            email VARCHAR(255),
            message TEXT,
            date VARCHAR(255)
        )''')\n""")
        new_lines.append(line)
    elif "def get_orders():" in line:
        new_lines.append("""def add_contact_message(name, email, message):
    try:
        from datetime import datetime
        conn = get_db()
        c = conn.cursor()
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO contact_messages (name, email, message, date) VALUES (?, ?, ?, ?)", (name, email, message, date))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Contact Error: {e}")

def get_contact_messages():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM contact_messages ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        return []\n\n""")
        new_lines.append(line)
    else:
        new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Backend contact logic integrated seamlessly.")
