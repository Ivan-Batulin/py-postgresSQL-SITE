"""
MIRMEX - Database Initialization

PostgreSQL database setup utility for MIRMEX tire online store.

This module provides:
- Database table creation for products and orders
- Initial product data population from JSON
- Duplicate record cleanup functionality
- Database connection management
"""

import psycopg2
import json
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import host, user, password, db_name, port


def create_tables():
    """
    Create database tables for products and orders.

    Creates two main tables in PostgreSQL database:
    - products: stores tire product information
    - orders: stores customer order data with foreign key reference

    The function uses IF NOT EXISTS clause to prevent errors
    if tables already exist.

    Tables created:
        products:
        - id: Primary key, auto-incrementing integer
        - name: Product name, unique constraint
        - description: Product description text
        - price: Product price (decimal)
        - width: Tire width in millimeters
        - image_url: URL to product image

        orders:
        - id: Primary key, auto-incrementing integer
        - product_id: Foreign key reference to products table
        - quantity: Number of items ordered
        - customer_name: Customer's full name
        - phone: Customer's phone number
        - email: Customer's email address
        - created_at: Order timestamp (auto-generated)

    Raises:
        psycopg2.Error: If database connection or table creation fails
        Exception: For any other errors during execution
    """
    conn = psycopg2.connect(host=host, user=user, password=password, dbname=db_name, port=port)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            price NUMERIC(10,2),
            width INT,
            image_url TEXT
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            product_id INT REFERENCES products(id),
            quantity INT,
            customer_name VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    conn.close()
    print("Tables created successfully")


def add_products():
    """
    Add predefined products to the products table.

    Inserts a set of predefined tire products into the database.
    Each product includes detailed specifications and image URLs.
    The function checks for existing products by name to avoid duplicates.

    Products included:
    - Mirage MR-166: Summer tires for passenger cars
    - TurboDrive V5: Premium summer tires with enhanced durability
    - RoadMaster Pro: Professional tires for commercial vehicles
    - WinterGrip Ice: Winter tires with improved ice traction
    - AllSeason Plus: All-season tires for year-round use

    Each product record contains:
    - name: Product model name
    - description: Detailed product description
    - price: Product price in UAH
    - width: Tire width specification
    - image_url: High-quality product image URL

    The function handles database transactions and provides
    detailed feedback on insertion results.

    Raises:
        psycopg2.Error: If database insertion operation fails
        Exception: For any other errors during the process
    """
    products = [
        ("Mirage MR-166", "High-quality summer tires Mirage MR-166 155/70 R13 73T for passenger vehicles", 1056.00, 155,
         "https://cdn.pixabay.com/photo/2020/02/09/11/09/tire-4833103_1280.jpg"),
        ("TurboDrive V5", "Premium summer tires TurboDrive V5 with enhanced durability and stylish design", 1250.00, 165,
         "https://cdn.pixabay.com/photo/2017/01/06/19/15/wheel-1954170_1280.jpg"),
        ("RoadMaster Pro", "Professional tires RoadMaster Pro for commercial vehicle applications", 890.00, 185,
         "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400"),
        ("WinterGrip Ice", "Winter tires WinterGrip Ice with improved traction on ice surfaces", 1450.00, 175,
         "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=400"),
        ("AllSeason Plus", "All-season tires AllSeason Plus for year-round vehicle operation", 980.00, 195,
         "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=400")
    ]

    conn = psycopg2.connect(host=host, user=user, password=password, dbname=db_name, port=port)
    conn.autocommit = True

    with conn.cursor() as cur:
        for product in products:
            name = product[0]
            cur.execute("SELECT id FROM products WHERE name = %s;", (name,))
            existing = cur.fetchone()

            if existing:
                print(f"Product '{name}' already exists (ID: {existing[0]})")
            else:
                try:
                    cur.execute("""
                        INSERT INTO products (name, description, price, width, image_url)
                        VALUES (%s, %s, %s, %s, %s)
                    """, product)
                    print(f"Product '{name}' added successfully")
                except psycopg2.Error as e:
                    print(f"Error adding product '{name}': {e}")

    conn.close()
    print("Product addition process completed")


def cleanup_duplicates():
    """
    Remove duplicate product records from database.

    Identifies and removes duplicate product entries based on product name,
    keeping only the record with the lowest ID for each unique name.
    This ensures data integrity and prevents redundant records.

    The cleanup process:
    1. Identifies duplicate records by product name
    2. Keeps the record with the minimum ID for each name
    3. Removes all other duplicate records
    4. Reports the number of deleted records

    This function is useful for maintaining clean database state
    after bulk import operations or data migration.

    Raises:
        psycopg2.Error: If database deletion operation fails
        Exception: For any other errors during the cleanup process
    """
    conn = psycopg2.connect(host=host, user=user, password=password, dbname=db_name, port=port)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM products
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM products
                GROUP BY name
            );
        """)
        deleted_count = cur.rowcount
        print(f"Duplicate records removed: {deleted_count}")

    conn.close()


if __name__ == "__main__":
    """
    Main execution block for database initialization.

    Orchestrates the complete database setup process:
    1. Creates required database tables
    2. Removes any existing duplicate records
    3. Populates tables with initial product data

    This script should be run after database creation and
    before starting the web application.
    """
    create_tables()
    cleanup_duplicates()
    add_products()
