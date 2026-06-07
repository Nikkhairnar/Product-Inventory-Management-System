# 📦 Product Inventory Management System

## One-Line Summary
A full-featured Product Inventory Management System built with Flask, SQLAlchemy, and a dark-themed UI — supporting complete CRUD operations, category management, search/filter, dashboard stats, and low-stock alerts.

---

## ✨ Features

- ✅ **Full CRUD** — Add, View, Edit, and Delete products
- 🔍 **Search & Filter** — Search by name or filter by category
- 📊 **Dashboard Stats** — Total products, total inventory value, low-stock count, and active categories
- ⚠️ **Low Stock Alerts** — Instantly see products with fewer than 10 units
- 🗂️ **Category Management** — 9 built-in categories (Electronics, Clothing, Books, Sports, and more)
- 🌐 **Multi-Database Support** — Works with SQLite, PostgreSQL, and MySQL via environment config
- 🎨 **Dark UI** — GitHub-inspired dark theme with responsive layout

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3, Flask                   |
| ORM        | Flask-SQLAlchemy                  |
| Database   | SQLite (default) / PostgreSQL / MySQL |
| Frontend   | HTML5, CSS3 (Vanilla, dark theme) |
| Templating | Jinja2                            |
| Config     | python-dotenv (.env file)         |

---

## 📁 Project Structure

```
Product-Inventory-Management-System/
├── app.py              ← Flask app: routes, models, DB config
├── .env.example        ← Example environment variables file
├── inventory.db        ← SQLite database (auto-created)
├── templates/
│   ├── index.html      ← Dashboard: product list, search, stats
│   ├── add.html        ← Add new product form
│   ├── edit.html       ← Edit existing product form
│   ├── product.html    ← Product detail view
│   └── low_stock.html  ← Low stock alerts page
└── README.md
```

---

## ⚙️ Prerequisites

- Python 3.8+
- pip

Install required packages:

```bash
pip install flask flask-sqlalchemy python-dotenv
```

For PostgreSQL support:
```bash
pip install psycopg2-binary
```

For MySQL support:
```bash
pip install pymysql
```

---

## 🚀 How to Run

### With SQLite (Default — No setup required):

```bash
# 1. Clone the repository
git clone https://github.com/Nikkhairnar/Product-Inventory-Management-System.git
cd Product-Inventory-Management-System

# 2. Install dependencies
pip install flask flask-sqlalchemy python-dotenv

# 3. Run the app
python app.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### With PostgreSQL:

```bash
# 1. Install PostgreSQL driver
pip install psycopg2-binary

# 2. Create .env file
cp .env.example .env

# 3. Edit .env and set your PostgreSQL URL
DATABASE_URL=postgresql://postgres:password@localhost:5432/inventory_db

# 4. Run the app
python app.py
```

**Setting up the PostgreSQL database:**

```bash
# Access PostgreSQL
psql -U postgres

# Create the database
CREATE DATABASE inventory_db;

# Exit
\q
```

---

### With MySQL:

```bash
# 1. Install MySQL driver
pip install pymysql

# 2. Create .env file
cp .env.example .env

# 3. Edit .env and set your MySQL URL
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/inventory_db

# 4. Run the app
python app.py
```

**Setting up the MySQL database:**

```bash
# Access MySQL
mysql -u root -p

# Create the database
CREATE DATABASE inventory_db;

# Exit
exit
```

---

## 🔐 Environment Variables

### Option 1: `.env` file (Recommended).

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env`:

```env
SECRET_KEY=your-random-secret-key
DATABASE_URL=sqlite:///inventory.db
FLASK_DEBUG=True
```

### Option 2: Terminal (temporary)

```bash
# Linux / macOS
export DATABASE_URL=postgresql://...
export SECRET_KEY=your-secret-key

# Windows
set DATABASE_URL=postgresql://...
set SECRET_KEY=your-secret-key
```

---

## 🗄️ Database URL Formats

| Database   | URL Format                                          |
|------------|-----------------------------------------------------|
| SQLite     | `sqlite:///inventory.db`                            |
| PostgreSQL | `postgresql://user:password@localhost:5432/dbname`  |
| MySQL      | `mysql+pymysql://user:password@localhost:3306/dbname` |

---

## 📊 Dashboard Overview

The main dashboard (`/`) displays:

| Stat              | Description                              |
|-------------------|------------------------------------------|
| Total Products    | Count of all products in inventory       |
| Total Value       | Sum of `price × stock` across all items  |
| Low Stock Alerts  | Products with fewer than 10 units        |
| Categories Used   | Number of distinct categories in use     |

---

## 🔁 CRUD Routes

| Route                  | Method      | Description              |
|------------------------|-------------|--------------------------|
| `/`                    | GET         | Dashboard & product list |
| `/product/<id>`        | GET         | View product details     |
| `/add`                 | GET, POST   | Add a new product        |
| `/edit/<id>`           | GET, POST   | Edit an existing product |
| `/delete/<id>`         | POST        | Delete a product         |
| `/low-stock`           | GET         | View low stock alerts    |

---

## 🏷️ Product Categories

Products can be assigned to one of the following categories:

`Electronics` · `Clothing` · `Food & Beverages` · `Home & Garden` · `Sports` · `Books` · `Toys` · `Health & Beauty` · `Other`

---

## 📦 Stock Status Logic

| Status       | Condition          | UI Colour |
|--------------|--------------------|-----------|
| ✅ In Stock   | `stock >= 10`      | Green     |
| ⚠️ Low Stock  | `0 < stock < 10`   | Yellow    |
| ❌ Out of Stock | `stock == 0`     | Red       |

---

## 🧪 Sample Data

On first run, the app automatically seeds **12 sample products** across multiple categories, including:

- MacBook Pro 16", Wireless Mouse, Mechanical Keyboard *(Electronics)*
- Running Shoes, Yoga Mat, Water Bottle *(Sports)*
- Python Crash Course *(Books)*
- Coffee Beans, Vitamin C Tablets, and more

---

## 🔌 Connection Pool Settings

For production databases, the app is pre-configured with:

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,       # Max open connections
    'pool_recycle': 3600,  # Recycle connections after 1 hour
    'pool_pre_ping': True, # Verify connection before use
}
```

---

## 🆚 SQLite vs PostgreSQL vs MySQL

| Feature       | SQLite              | PostgreSQL         | MySQL              |
|---------------|---------------------|--------------------|--------------------|
| Setup         | None required       | Server needed      | Server needed      |
| Best For      | Development / Local | Production         | Production         |
| Concurrency   | Limited             | Excellent          | Good               |
| Performance   | Fast (small data)   | Excellent          | Excellent          |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Nikkhairnar**  
GitHub: [@Nikkhairnar](https://github.com/Nikkhairnar)
