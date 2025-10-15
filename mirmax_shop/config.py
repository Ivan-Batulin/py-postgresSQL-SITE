"""
MIRMEX - Database Configuration

PostgreSQL connection settings for MIRMEX tire online store.
Contains all necessary parameters for database connectivity.

Configuration Parameters:
    host (str): PostgreSQL server hostname or IP address
                Default: "127.0.0.1" (localhost)

    user (str): PostgreSQL username for authentication
                Default: "postgres" (standard PostgreSQL admin user)

    password (str): PostgreSQL user password for authentication
                    IMPORTANT: Change this to your actual PostgreSQL password
                    Default: "12313131" (example password)

    db_name (str): Target database name for MIRMEX application
                   Default: "shop_db" (shop database)

    port (int): PostgreSQL server port number
                Default: 5432 (standard PostgreSQL port)

Security Note:
    Never commit actual passwords to version control.
    Use environment variables or secure configuration management
    for production deployments.

Database Setup Requirements:
    1. PostgreSQL server must be running
    2. Database 'shop_db' must exist
    3. User must have full privileges on the database
    4. Tables will be created automatically by init_db.py
"""

# Database connection settings
host = "127.0.0.1"
user = "postgres"
password = "12313213"
db_name = "shop_db"
port = 5432
