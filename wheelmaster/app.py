"""
WheelMaster - Tire Online Store

Main Flask application for tire online store with JSON product loading
and PostgreSQL order storage functionality.

This module handles:
- Web interface rendering
- Product data management from JSON
- Order processing and database storage
- PostgreSQL database integration
"""

import json
import os
import sys
from flask import Flask, render_template, request
import psycopg2

# Добавляем текущую директорию в путь для импорта config
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from config import host, user, password, db_name, port

app = Flask(__name__,
           template_folder='templates',
           static_folder='static')
def load_products():
    """
    Load products from JSON file.

    Reads product data from products.json file and returns
    a list of product dictionaries for template rendering.

    Returns:
        list: List of product dictionaries containing id, name, description,
    Raises:
        FileNotFoundError: If products.json file doesn't exist.
        json.JSONDecodeError: If JSON file is malformed.
    """
    json_path = os.path.join(os.path.dirname(__file__), 'products.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['products']
def save_order_to_postgres(product_id, quantity, customer_name, phone, email):
    """
    Save order to PostgreSQL database.

    Creates a new order record in the orders table with the provided
    customer and product information.

    Args:
        product_id (int): ID of the product being ordered
        quantity (int): Quantity of products ordered
        customer_name (str): Name of the customer
        phone (str): Customer's phone number
        email (str): Customer's email address

    Returns:
        bool: True if order was saved successfully, False otherwise

    Raises:
        psycopg2.Error: If database operation fails
        Exception: For any other errors during the process
    """
    try:
        print(f"Attempting to save order to PostgreSQL: product={product_id}, quantity={quantity}, customer={customer_name}")
        connection = psycopg2.connect(host=host, user=user, password=password, dbname=db_name, port=port)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO orders (product_id, quantity, customer_name, phone, email)
                VALUES (%s, %s, %s, %s, %s)
            """, (product_id, quantity, customer_name, phone, email))
            print("Order successfully saved to PostgreSQL!")

        connection.close()
        return True
    except Exception as e:
        print(f"Error saving order to PostgreSQL: {e}")
        return False


@app.route("/")
def index():
    """
    Main page displaying all products.

    Renders the main page with a grid of all available products
    loaded from the database and JSON configuration.

    Returns:
        str: Rendered HTML template with products data
    """
    products = load_products()
    return render_template("index.html", products=products)


@app.route("/order/<int:product_id>", methods=["GET", "POST"])
def order(product_id):
    """
    Product order page with form handling.

    Displays product details and handles order form submission.
    On POST request, validates and saves the order to database.

    Args:
        product_id (int): ID of the product to display/order

    Returns:
        str: Rendered HTML template or success/error message

    Raises:
        404: If product with given ID is not found
    """
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)

    if not product:
        return "Product not found", 404

    if request.method == "POST":
        quantity = int(request.form["quantity"])
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]

        print("Attempting to save to PostgreSQL...")
        postgres_saved = save_order_to_postgres(product_id, quantity, name, phone, email)

        if postgres_saved:
            print("Order successfully saved to PostgreSQL!")
            return "<h2 style='color:#27ae60; text-align:center; margin:50px;'>✅ Order accepted! We will contact you soon.</h2>"
        else:
            print("Failed to save order to PostgreSQL")
            return "<h2 style='color:#e74c3c; text-align:center; margin:50px;'>⚠️ Database problem occurred. Please try again later.</h2>"

    return render_template("order.html", product=product)


if __name__ == "__main__":
    """
    Application entry point.

    Starts the Flask development server with debug mode enabled.
    Server runs on localhost:5000 by default.
    """
    app.run(host="127.0.0.1", port=5000, debug=True)
