"""
Product Inventory Management System
=====================================
Full CRUD operations with Flask + SQLAlchemy

Features:
- Add, View, Edit, Delete products (full CRUD)
- Category management
- Search and filter
- Dashboard stats
- Low-stock alerts
- Environment-based DB config (SQLite / PostgreSQL / MySQL)
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///inventory.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}

db = SQLAlchemy(app)


# =============================================================================
# MODEL
# =============================================================================

CATEGORIES = [
    'Electronics', 'Clothing', 'Food & Beverages',
    'Home & Garden', 'Sports', 'Books', 'Toys', 'Health & Beauty', 'Other'
]

class Product(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    category    = db.Column(db.String(100), default='Other')
    price       = db.Column(db.Float, nullable=False)
    stock       = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Product {self.name}>'

    @property
    def total_value(self):
        return self.price * self.stock

    @property
    def stock_status(self):
        if self.stock == 0:
            return 'out'
        elif self.stock < 10:
            return 'low'
        else:
            return 'ok'


# =============================================================================
# HELPER
# =============================================================================

def get_db_type():
    url = DATABASE_URL.lower()
    if 'postgresql' in url or 'postgres' in url:
        return 'PostgreSQL'
    elif 'mysql' in url:
        return 'MySQL'
    return 'SQLite'


# =============================================================================
# ROUTES — READ (List / Dashboard)
# =============================================================================

@app.route('/')
def index():
    search   = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if category:
        query = query.filter(Product.category == category)

    products = query.order_by(Product.name).all()

    # Dashboard stats
    all_products  = Product.query.all()
    total_products = len(all_products)
    total_value    = sum(p.total_value for p in all_products)
    low_stock_count = Product.query.filter(Product.stock < 10).count()
    categories_used = db.session.query(Product.category).distinct().count()

    return render_template(
        'index.html',
        products=products,
        categories=CATEGORIES,
        db_type=get_db_type(),
        db_url=DATABASE_URL,
        search=search,
        selected_category=category,
        total_products=total_products,
        total_value=total_value,
        low_stock_count=low_stock_count,
        categories_used=categories_used,
    )


# =============================================================================
# ROUTES — READ (Detail)
# =============================================================================

@app.route('/product/<int:id>')
def view_product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)


# =============================================================================
# ROUTES — CREATE
# =============================================================================

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name     = request.form['name'].strip()
        category = request.form.get('category', 'Other')
        price    = float(request.form['price'])
        stock    = int(request.form.get('stock', 0))
        desc     = request.form.get('description', '').strip()

        if not name:
            flash('Product name is required.', 'danger')
            return render_template('add.html', categories=CATEGORIES)

        new_product = Product(
            name=name, category=category,
            price=price, stock=stock, description=desc
        )
        db.session.add(new_product)
        db.session.commit()
        flash(f'✅ Product "{name}" added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html', categories=CATEGORIES)


# =============================================================================
# ROUTES — UPDATE
# =============================================================================

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name        = request.form['name'].strip()
        product.category    = request.form.get('category', 'Other')
        product.price       = float(request.form['price'])
        product.stock       = int(request.form.get('stock', 0))
        product.description = request.form.get('description', '').strip()

        if not product.name:
            flash('Product name is required.', 'danger')
            return render_template('edit.html', product=product, categories=CATEGORIES)

        db.session.commit()
        flash(f'✅ Product "{product.name}" updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', product=product, categories=CATEGORIES)


# =============================================================================
# ROUTES — DELETE
# =============================================================================

@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f'🗑️ Product "{name}" deleted.', 'danger')
    return redirect(url_for('index'))


# =============================================================================
# ROUTES — LOW STOCK ALERT
# =============================================================================

@app.route('/low-stock')
def low_stock():
    products = Product.query.filter(Product.stock < 10).order_by(Product.stock).all()
    return render_template('low_stock.html', products=products)


# =============================================================================
# INITIALIZE DATABASE WITH SAMPLE DATA
# =============================================================================

def init_db():
    with app.app_context():
        db.create_all()
        print(f'✅ Database initialized! Using: {DATABASE_URL}')

        if Product.query.count() == 0:
            sample = [
                Product(name='MacBook Pro 16"',  category='Electronics',     price=2499.99, stock=8,   description='Apple M3 Pro chip, 18GB RAM, 512GB SSD'),
                Product(name='Wireless Mouse',   category='Electronics',     price=39.99,   stock=45,  description='Ergonomic silent wireless mouse'),
                Product(name='Mechanical Keyboard', category='Electronics',  price=119.99,  stock=25,  description='RGB backlit, Cherry MX switches'),
                Product(name='USB-C Hub',         category='Electronics',     price=49.99,   stock=3,   description='7-in-1 hub with HDMI, USB 3.0, SD card'),
                Product(name='Monitor 27"',       category='Electronics',     price=349.99,  stock=12,  description='4K IPS display, 144Hz refresh rate'),
                Product(name='Running Shoes',     category='Sports',          price=89.99,   stock=30,  description='Lightweight mesh upper, cushioned sole'),
                Product(name='Yoga Mat',          category='Sports',          price=29.99,   stock=0,   description='Non-slip, eco-friendly material'),
                Product(name='Water Bottle',      category='Sports',          price=24.99,   stock=60,  description='Insulated stainless steel, 1L'),
                Product(name='Python Crash Course', category='Books',         price=34.99,   stock=20,  description='Best-seller programming guide for beginners'),
                Product(name='Desk Lamp LED',     category='Home & Garden',   price=44.99,   stock=5,   description='Touch-sensitive, 3 colour temperatures'),
                Product(name='Coffee Beans 1kg',  category='Food & Beverages',price=19.99,   stock=100, description='Single-origin Arabica, medium roast'),
                Product(name='Vitamin C Tablets', category='Health & Beauty', price=12.99,   stock=7,   description='500mg, pack of 60 tablets'),
            ]
            db.session.add_all(sample)
            db.session.commit()
            print(f'✅ {len(sample)} sample products added!')


if __name__ == '__main__':
    init_db()
    app.run(debug=os.getenv('FLASK_DEBUG', 'True') == 'True')
