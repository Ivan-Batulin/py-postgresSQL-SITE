"""
WheelMaster - Order Viewer

PostgreSQL order management utility for WheelMaster tire online store.

This module provides:
- Order history retrieval from database
- Customer order information display
- Order statistics and reporting
- Database connection management
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mirmax_shop.config import host, user, password, db_name, port


def view_all_orders():
    """
    Retrieve and display all orders from PostgreSQL database.

    Establishes connection to PostgreSQL database and performs comprehensive
    order data retrieval with joined product information for complete analysis.

    Database operations:
    1. Retrieves total order count for statistics
    2. Fetches detailed order information including:
       - Order ID and timestamp
       - Customer contact information
       - Product details (name, price)
       - Order quantity and total value calculation

    Display format includes:
    - Order count summary
    - Detailed order breakdown with customer info
    - Product correlation data
    - Total order value calculation
    - Chronological sorting (newest first)

    Each order display contains:
    - Order number and creation date
    - Customer name, phone, and email
    - Product name and unit price
    - Quantity ordered and total amount
    - Formatted output with clear section dividers

    The function handles empty order scenarios and provides
    appropriate user feedback.

    Returns:
        None: Prints formatted order data directly to console

    Raises:
        psycopg2.Error: If database connection or query execution fails
        Exception: For any other errors during the process
    """
    try:
        connection = psycopg2.connect(host=host, user=user, password=password, dbname=db_name, port=port)

        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM orders;')
            count = cursor.fetchone()[0]
            print(f'Total orders in PostgreSQL: {count}')

            if count == 0:
                print('No orders found in orders table yet')
            else:
                cursor.execute('''
                    SELECT
                        o.id,
                        o.quantity,
                        o.customer_name,
                        o.phone,
                        o.email,
                        o.created_at,
                        p.name as product_name,
                        p.price
                    FROM orders o
                    JOIN products p ON o.product_id = p.id
                    ORDER BY o.created_at DESC;
                ''')

                orders = cursor.fetchall()

                print('\nComplete order history:')
                print('=' * 80)

                for order in orders:
                    order_id, quantity, customer_name, phone, email, created_at, product_name, price = order
                    total = quantity * price

                    print(f'Order #{order_id}')
                    print(f'Date: {created_at}')
                    print(f'Customer: {customer_name}')
                    print(f'Phone: {phone}')
                    print(f'Email: {email}')
                    print(f'Product: {product_name}')
                    print(f'Quantity: {quantity}')
                    print(f'Unit Price: {price} UAH')
                    print(f'Total Amount: {total} UAH')
                    print('-' * 80)

    except Exception as e:
        print(f'Database connection error: {e}')
        print('Please verify database connection settings in config.py')

    finally:
        if 'connection' in locals():
            connection.close()
            print('\nDatabase connection terminated')


if __name__ == "__main__":
    """
    Main execution block for order viewing functionality.

    Initiates the comprehensive order retrieval and display process,
    providing complete visibility into customer orders and purchase history.
    """
    view_all_orders()
