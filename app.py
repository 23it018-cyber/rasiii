import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ─── BACKEND IMPORT ───────────────────────────
from db_operations import *

app = Flask(__name__)
app.secret_key = 'rasiii_mart_secure_session_key'

# ─── AUTH ROUTES ─────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check Admin First
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            session['user'] = 'Admin'
            flash("Welcome to the Admin Dashboard", "success")
            return redirect(url_for('admin_dashboard'))

        # Check Regular User
        users = get_users()
        user = next((u for u in users if u.get('Username') == username and check_password_hash(str(u.get('Password')), password)), None)

        if user:
            session['user'] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials or user does not exist", "danger")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        users = get_users()
        if any(u.get('Username') == username for u in users):
            flash("Username already exists", "danger")
        else:
            hashed_password = generate_password_hash(password)
            add_user({"Username": username, "Email": email, "Password": hashed_password})
            session['user'] = username
            flash("Account created successfully!", "success")
            return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin_logged_in', None)
    flash("You have been logged out", "info")
    return redirect(url_for('home'))


# ─── CORE ROUTES ─────────────────────────────────────────────────────────────

@app.route('/')
def home():
    products = get_products()
    contacts = get_contact_messages()
    offers = [p for p in products if p.get('Category') in ['Fruits & Vegetables', 'Household Essentials', 'Dairy Products']][:6]
    return render_template('home.html', offers=offers)

@app.route('/shop')
def shop():
    products = get_products()
    contacts = get_contact_messages()
    categorized_products = {}
    for p in products:
        cat = p.get('Category')
        if not cat: continue
        if cat not in categorized_products:
            categorized_products[cat] = []
        categorized_products[cat].append(p)
    return render_template('shop.html', categories=categorized_products)

@app.route('/api/add-to-cart', methods=['POST'])
def api_add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    data = request.json
    product_id = data.get('product_id')
    product = get_product_by_id(product_id)

    if product:
        pid_str = str(product_id)
        if pid_str in session['cart']:
            session['cart'][pid_str]['quantity'] += 1
        else:
            session['cart'][pid_str] = {
                'name': product.get('Name'),
                'price': float(product.get('Price', 0)),
                'quantity': 1,
                'category': product.get('Category'),
                'unit': product.get('Unit', '')
            }
        session.modified = True

        cart_count = sum(item['quantity'] for item in session['cart'].values())
        return jsonify({
            'status': 'success',
            'message': f"{product.get('Name')} added to cart!",
            'cart_count': cart_count
        })

    return jsonify({'status': 'error', 'message': 'Product not found'}), 404

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' not in session:
        session['cart'] = {}

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        action = request.form.get('action')

        if action == 'remove':
            pid_str = str(product_id)
            if pid_str in session['cart']:
                del session['cart'][pid_str]
                session.modified = True
                flash("Item removed from cart.", "info")
        elif action == 'update':
            pid_str = str(product_id)
            qty = int(request.form.get('quantity', 1))
            if pid_str in session['cart'] and qty > 0:
                session['cart'][pid_str]['quantity'] = qty
                session.modified = True
        elif action == 'apply_discount':
            code = request.form.get('discount_code', '').strip()
            percents = {
                '000000000000': 10,
                '111111111111111': 20,
                '333333333333333': 30,
                '444444444444444': 40,
                '555555555555555': 50
            }
            if code in percents:
                session['discount'] = percents[code]
                session['discount_code'] = code
                flash(f"Coupon applied: {percents[code]}% off!", "success")
            elif code.isdigit() and 0 < int(code) < 100:
                session['discount'] = int(code)
                session['discount_code'] = code + "% off"
                flash(f"Discount applied: {code}% off!", "success")
            else:
                session['discount'] = 0
                session.pop('discount_code', None)
                flash("Invalid or missing coupon code.", "danger")
        elif action == 'remove_discount':
            session['discount'] = 0
            session.pop('discount_code', None)
            flash("Coupon removed.", "info")
        return redirect(url_for('cart'))

    base_total = sum(item['price'] * item['quantity'] for item in session['cart'].values())
    discount_pct = session.get('discount', 0)
    discount_amount = base_total * (discount_pct / 100.0)
    total = base_total - discount_amount
    discount_code = session.get('discount_code')

    return render_template('cart.html', cart=session['cart'], base_total=base_total, discount_pct=discount_pct, discount_amount=discount_amount, total=total, discount_code=discount_code)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('shop'))

    base_total = sum(item['price'] * item['quantity'] for item in session['cart'].values())
    discount_pct = session.get('discount', 0)
    total = base_total - (base_total * (discount_pct / 100.0))

    if request.method == 'POST':
        session['checkout_info'] = {
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'delivery_date': request.form.get('delivery_date'),
            'recommended_date': request.form.get('recommended_date'),
            'total': total
        }
        return redirect(url_for('payment'))

    from datetime import timedelta
    rec_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    return render_template('checkout.html', total=total, rec_date=rec_date)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'checkout_info' not in session:
        return redirect(url_for('cart'))

    if request.method == 'POST':
        info = session['checkout_info']
        items_str = ", ".join([f"{v['name']} ({v['quantity']} {v.get('unit', '')})" for k, v in session['cart'].items()])

        order_data = {
            "Order ID": f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "Customer Name": info.get('name'),
            "Phone": info.get('phone'),
            "Address": info.get('address'),
            "Delivery Date": info.get('delivery_date', 'Not Specified') + " (Est: 1-2 Days)",
            "Items": items_str,
            "Total Amount": info.get('total'),
            "Date": datetime.now().strftime('%Y-%m-%d'),
            "Time": datetime.now().strftime('%H:%M:%S'),
            "Status": "Order Placed"
        }

        add_order(order_data)
        update_stock(session['cart'])

        session.pop('cart', None)
        session.pop('checkout_info', None)
        return redirect(url_for('order_success', order_id=order_data['Order ID']))

    return render_template('payment.html', total=session['checkout_info'].get('total', 0))

@app.route('/order-success/<order_id>')
def order_success(order_id):
    return render_template('order_success.html', order_id=order_id)

@app.route('/track-order', methods=['GET', 'POST'])
def track_order():
    order = None
    if request.method == 'POST':
        order_id = request.form.get('order_id').strip()
        orders = get_orders()
        order = next((o for o in orders if o.get('Order ID') == order_id), None)
        if not order:
            flash("Order ID not found.", "danger")
    return render_template('track_order.html', order=order)

@app.route('/prev-orders')
def prev_orders():
    if 'user' not in session:
        flash("Please login to view your previous orders.", "warning")
        return redirect(url_for('login'))
    
    username = session['user']
    all_orders = get_orders()
    # Filter orders by current logged in user
    # If the database doesn't have a specific 'Username' column, we match by 'Customer Name'
    # but for a real app we'd use a foreign key. Here we'll check if the schema handles it or match by name.
    user_orders = [o for o in all_orders if o.get('Customer Name') == username]
    
    return render_template('prev_orders.html', orders=user_orders)

@app.route('/contact', methods=['GET', 'POST'])
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


# ─── ADMIN ROUTES ─────────────────────────────────────────────────────────────

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    orders = get_orders()
    products = get_products()
    contacts = get_contact_messages()

    daily_revenue = {}
    total_sales = 0

    for order in orders:
        date = order.get('Date', 'Unknown')
        amount = float(order.get('Total Amount', 0))
        total_sales += amount

        if date not in daily_revenue:
            daily_revenue[date] = {'total': 0, 'order_count': 0, 'orders': []}

        daily_revenue[date]['total'] += amount
        daily_revenue[date]['order_count'] += 1
        daily_revenue[date]['orders'].append(order)

    sorted_dates = sorted(daily_revenue.keys(), reverse=True)

    return render_template('admin_dashboard.html',
                           orders=orders,
                           products=products,
                           daily_revenue=daily_revenue,
                           sorted_dates=sorted_dates,
                           total_sales=total_sales,
                           contacts=contacts)

@app.route('/admin/products/add', methods=['POST'])
def add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    category = request.form.get('category')
    name = request.form.get('name')
    price = float(request.form.get('price'))
    stock = int(request.form.get('stock'))
    unit = request.form.get('unit', '')
    image = get_image_for_product(name, category)
    
    try:
        new_id = get_max_product_id() + 1
        add_product_direct(new_id, category, name, price, stock, image, unit)
        flash("Product added successfully", "success")
    except Exception as e:
        flash(f"Error adding product: {e}", "danger")
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/products/delete/<int:pid>')
def delete_product(pid):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    try:
        delete_product_direct(pid)
        flash("Product deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting product: {e}", "danger")
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/orders/update-status', methods=['POST'])
def update_order_status():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    order_id = request.form.get('order_id')
    new_status = request.form.get('status')
    
    try:
        update_order_status_direct(order_id, new_status)
        flash(f"Order {order_id} updated to {new_status}", "success")
    except Exception as e:
        flash(f"Error updating order status: {e}", "danger")
        
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    # Initialize DB (creates default records if not present)
    init_db()
    
    app.run(debug=True, port=5000)
