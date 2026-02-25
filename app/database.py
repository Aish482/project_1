"""
Database connection and schema management module.
Handles MySQL database connection and table creation.
"""

import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'logistic'
}


def get_connection():
    """
    Establish and return a MySQL database connection.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
        
    Raises:
        Error: If connection fails
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        logger.info("Database connection successful")
        return conn
    except Error as e:
        logger.error(f"Error connecting to database: {e}")
        raise


def create_tables():
    """
    Create all required tables in the database if they don't exist.
    Establishes proper relationships and indexes for optimization.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create shipments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shipments (
                shipment_id VARCHAR(50) PRIMARY KEY,
                order_date DATE NOT NULL,
                origin VARCHAR(100) NOT NULL,
                destination VARCHAR(100) NOT NULL,
                weight DECIMAL(10, 2) NOT NULL,
                courier_id VARCHAR(50),
                status VARCHAR(50) NOT NULL,
                delivery_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_status (status),
                INDEX idx_courier_id (courier_id),
                INDEX idx_order_date (order_date),
                INDEX idx_origin_destination (origin, destination)
            )
        """)
        logger.info("Shipments table created")
        
        # Create shipment_tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shipment_tracking (
                tracking_id INT AUTO_INCREMENT PRIMARY KEY,
                shipment_id VARCHAR(50) NOT NULL,
                status VARCHAR(50) NOT NULL,
                timestamp DATETIME NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_shipment_id (shipment_id),
                INDEX idx_status (status),
                INDEX idx_timestamp (timestamp),
                FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
            )
        """)
        logger.info("Shipment_tracking table created")
        
        # Create courier_staff table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courier_staff (
                courier_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                rating DECIMAL(3, 1),
                vehicle_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_rating (rating),
                INDEX idx_vehicle_type (vehicle_type)
            )
        """)
        logger.info("Courier_staff table created")
        
        # Create routes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS routes (
                route_id VARCHAR(50) PRIMARY KEY,
                origin VARCHAR(100) NOT NULL,
                destination VARCHAR(100) NOT NULL,
                distance_km DECIMAL(10, 2) NOT NULL,
                avg_time_hours DECIMAL(5, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_origin_destination (origin, destination),
                INDEX idx_distance (distance_km)
            )
        """)
        logger.info("Routes table created")
        
        # Create warehouses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS warehouses (
                warehouse_id VARCHAR(50) PRIMARY KEY,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(50),
                capacity INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_city (city),
                INDEX idx_state (state)
            )
        """)
        logger.info("Warehouses table created")
        
        # Create costs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS costs (
                shipment_id VARCHAR(50) PRIMARY KEY,
                fuel_cost DECIMAL(15, 2),
                labor_cost DECIMAL(15, 2),
                misc_cost DECIMAL(15, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_fuel_cost (fuel_cost),
                FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
            )
        """)
        logger.info("Costs table created")
        
        conn.commit()
        logger.info("All tables created successfully")
        cursor.close()
        conn.close()
        
    except Error as e:
        logger.error(f"Error creating tables: {e}")
        raise


def drop_all_tables():
    """
    Drop all tables from the database (use with caution).
    Useful for resetting the database during development.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        tables = ['shipment_tracking', 'costs', 'shipments', 'courier_staff', 'routes', 'warehouses']
        
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            logger.info(f"Dropped table {table}")
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("All tables dropped successfully")
        
    except Error as e:
        logger.error(f"Error dropping tables: {e}")
        raise


if __name__ == "__main__":
    # Reset and create fresh tables
    # Uncomment the next line only if you want to drop existing tables
    # drop_all_tables()
    create_tables()

