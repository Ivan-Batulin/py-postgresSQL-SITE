# MIRMEX - Tire Online Store

![MIRMEX](https://img.shields.io/badge/MIRMEX-Tire--Online--Store-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

Modern tire online store with professional design, PostgreSQL database and convenient interface for product and order management.

## 🚀 Features

- **Beautiful web interface** with responsive design
- **PostgreSQL database** for storing products and orders
- **Product management** through JSON file
- **Order system** with database storage
- **Custom wheel icon** in the header
- **Professional design** with gradients and animations

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [API](#api)
- [License](#license)

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **PostgreSQL 12+**
- **Git**

### Step 1: Clone the Project

```bash
git clone https://github.com/your-username/mirmex-tire-shop.git
cd mirmex-tire-shop
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Database Configuration

Open the `config.py` file and configure the PostgreSQL connection parameters:

```python
host = "localhost"
user = "postgres"
password = "your_password"
db_name = "shop_db"
port = 5432
```

### Step 4: Initialize the Database

```bash
python init_db.py
```

### Step 5: Run the Application

```bash
python main.py
```

Open your browser and navigate to `http://127.0.0.1:5000`

## 📦 Installation

### Automated Installation (Linux/Mac)

```bash
# Clone the project
git clone https://github.com/your-username/mirmex-tire-shop.git
cd mirmex-tire-shop

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# PostgreSQL setup
sudo -u postgres createdb shop_db
sudo -u postgres psql -c "CREATE USER your_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE shop_db TO your_user;"

# Initialize database
python init_db.py

# Run the application
python main.py
```

### Manual PostgreSQL Setup

1. **Install PostgreSQL** from the official website
2. **Create the database:**
   ```sql
   CREATE DATABASE shop_db;
   CREATE USER your_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE shop_db TO your_user;
   ```
3. **Update `config.py`** with your parameters
4. **Run initialization:** `python init_db.py`

## 🗄️ Database Setup

### Database Structure

#### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    price NUMERIC(10,2),
    width INT,
    image_url TEXT
);
```

#### Orders Table
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    quantity INT,
    customer_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Product Management

Products are stored in the `products.json` file. Structure:

```json
{
  "products": [
    {
      "id": 1,
      "name": "Product Name",
      "description": "Product description",
      "price": 1000.00,
      "width": 155,
      "image_url": "image_link",
      "specifications": {
        "Code": "MR-166",
        "Size": "155/70 R13",
        "Season": "Summer"
      }
    }
  ]
}
```

## 🚀 Running the Project

### Development Mode

```bash
python main.py
```

The application will start at `http://127.0.0.1:5000` with debug mode enabled.

### Production Mode

```bash
python -c "from main import app; app.run(host='0.0.0.0', port=5000)"
```

### Database Status Check

```bash
# Product count
python check_db.py

# Order list
python view_orders.py
```

## 📁 Project Structure

```
mirmex-tire-shop/
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── config.py              # Database connection settings
├── main.py               # Main Flask application
├── init_db.py            # Database initialization
├── check_db.py           # Database product check
├── view_orders.py        # Order viewing
├── products.json         # Product data
├── static/               # Static files
│   └── style.css        # CSS styles
└── templates/           # HTML templates
    ├── index.html       # Main page
    └── order.html       # Order form page
```

## 🎯 Usage

### Adding a New Product

1. Open `products.json`
2. Add a new product to the `products` array
3. Run `python init_db.py` to update the database

### Order Processing

Orders are automatically saved to the `orders` table in PostgreSQL. To view:

```bash
python view_orders.py
```

### Design Customization

- **Colors and styles:** edit `static/style.css`
- **Page templates:** modify files in `templates/`
- **Logo:** replace in `templates/index.html`

## 🔌 API

### Main Page
```
GET /
```
Displays all products from the database.

### Product Page
```
GET /order/<product_id>
```
Order form for a specific product.

### Submit Order
```
POST /order/<product_id>
```
Saves the order to the PostgreSQL database.

## 🛠️ Development

### Adding New Features

1. Create a new function in `main.py`
2. Add the corresponding route
3. Update templates if necessary

### Working with Database

```python
from mirmax_shop.config import host, user, password, db_name, port
import psycopg2

# Connection
conn = psycopg2.connect(host=host, user=user, password=password, dbname=db_name, port=port)

# Working with cursor
with conn.cursor() as cursor:
   cursor.execute("SELECT * FROM products")
   products = cursor.fetchall()

conn.close()
```

## 📊 Monitoring

### Application Logs

The application logs all actions to the console when running in development mode.

### Database Check

```bash
# Product count
python check_db.py

# Recent orders
python view_orders.py
```

## 🐛 Troubleshooting

### PostgreSQL Connection Issues

1. **Check if PostgreSQL is running:**
   ```bash
   sudo systemctl status postgresql  # Linux
   # or
   services.msc  # Windows - find PostgreSQL
   ```

2. **Check parameters in `config.py`:**
   ```python
   host = "localhost"  # or server IP address
   port = 5432         # standard PostgreSQL port
   ```

3. **Check access rights:**
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE shop_db TO your_user;
   ```

### Application Launch Issues

1. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you encounter problems or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Create an Issue on GitHub
3. Write in the Discussions section

## 👥 Authors

- **Developer** - [IVAN BATULIN](https://github.com/Ivan-Batulin)

## 🙏 Acknowledgments

- Flask for the excellent web framework
- PostgreSQL for the reliable database
- All project contributors

---

⭐ **If you like this project, give it a star!**
