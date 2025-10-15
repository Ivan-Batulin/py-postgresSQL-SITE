"""
WheelMaster - Database Product Checker

Database diagnostic utility for
- Connection cleanup and error handling
"""

import psycopg2
from config import host, user, password, db_name, port


def check_database_products():
    """
    Check and display database product information.

    Establishes connection to PostgreSQL database and performs diagnostic
    queries to verify data integrity and provide inventory overview.

    Database queries performed:
    1. Product count verification
    2. Product details retrieval (ID, name, price)

    Output includes:
    - Total number of products in database
    - Detailed list of each product with ID, name, and price
    - Error reporting if connection or queries fail

    The function handles database connections safely with proper
    cleanup in case of errors.

    Returns:
        None: Prints results directly to console

    Raises:
        psycopg2.Error: If database connection or query execution fails
        Exception: For any other errors during execution
    """
    try:
        connection = psycopg2.connect(host=host, user=user, password=password, dbname=db_name, port=port)
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM products;')
            count = cursor.fetchone()[0]
            print(f'Total products in database: {count}')

            cursor.execute('SELECT id, name, price FROM products;')
            products = cursor.fetchall()
            print('\nProduct inventory:')
            for product in products:
                print(f'ID: {product[0]}, Name: {product[1]}, Price: {product[2]} UAH')

    except Exception as e:
        print(f'Database error: {e}')
        print('Please check database connection settings in config.py')
    finally:
        if 'connection' in locals():
            connection.close()
            print('Database connection closed')


if __name__ == "__main__":
    """
    Main execution block for database product checking.

    Initiates the database diagnostic process to verify product
    data integrity and provide inventory overview.
    """
    check_database_products()
