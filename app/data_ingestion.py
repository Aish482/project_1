"""
Data ingestion module for loading CSV and JSON files into MySQL database.
Handles parsing, validation, and batch insertion of logistics data.
"""

import csv
import json
import pandas as pd
from database import get_connection
import logging
from mysql.connector import Error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_SIZE = 500  # Insert records in batches for better performance


def load_json_file(filepath):
    """
    Load JSON data from file.
    
    Args:
        filepath (str): Path to JSON file
        
    Returns:
        list: List of dictionaries from JSON
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} records from {filepath}")
        return data
    except Exception as e:
        logger.error(f"Error loading JSON file {filepath}: {e}")
        raise


def load_csv_file(filepath):
    """
    Load CSV data from file.
    
    Args:
        filepath (str): Path to CSV file
        
    Returns:
        pandas.DataFrame: DataFrame with CSV data
    """
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} records from {filepath}")
        return df
    except Exception as e:
        logger.error(f"Error loading CSV file {filepath}: {e}")
        raise


def insert_shipments(json_file):
    """
    Insert shipment records from JSON file into shipments table.
    
    Args:
        json_file (str): Path to shipments.json
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        data = load_json_file(json_file)
        
        insert_query = """
            INSERT INTO shipments 
            (shipment_id, order_date, origin, destination, weight, courier_id, status, delivery_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """
        
        batch = []
        for i, record in enumerate(data):
            batch.append((
                record.get('shipment_id'),
                record.get('order_date'),
                record.get('origin'),
                record.get('destination'),
                record.get('weight'),
                record.get('courier_id'),
                record.get('status'),
                record.get('delivery_date')
            ))
            
            if len(batch) >= BATCH_SIZE or i == len(data) - 1:
                cursor.executemany(insert_query, batch)
                conn.commit()
                logger.info(f"Inserted {len(batch)} shipment records")
                batch = []
        
        cursor.close()
        conn.close()
        logger.info(f"Successfully inserted all shipment records from {json_file}")
        
    except Error as e:
        logger.error(f"Error inserting shipments: {e}")
        raise


def insert_shipment_tracking(csv_file):
    """
    Insert shipment tracking records from CSV file.
    
    Args:
        csv_file (str): Path to shipment_tracking.csv
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        df = load_csv_file(csv_file)
        
        insert_query = """
            INSERT INTO shipment_tracking 
            (tracking_id, shipment_id, status, timestamp)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """
        
        batch = []
        for i, row in df.iterrows():
            batch.append((
                row['tracking_id'],
                row['shipment_id'],
                row['status'],
                row['timestamp']
            ))
            
            if len(batch) >= BATCH_SIZE or i == len(df) - 1:
                cursor.executemany(insert_query, batch)
                conn.commit()
                logger.info(f"Inserted {len(batch)} tracking records")
                batch = []
        
        cursor.close()
        conn.close()
        logger.info(f"Successfully inserted all tracking records from {csv_file}")
        
    except Error as e:
        logger.error(f"Error inserting shipment tracking: {e}")
        raise


def insert_courier_staff(csv_file):
    """
    Insert courier staff records from CSV file.
    
    Args:
        csv_file (str): Path to courier_staff.csv
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        df = load_csv_file(csv_file)
        
        insert_query = """
            INSERT INTO courier_staff 
            (courier_id, name, rating, vehicle_type)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE rating = VALUES(rating)
        """
        
        batch = []
        for i, row in df.iterrows():
            batch.append((
                row['courier_id'],
                row['name'],
                row['rating'],
                row['vehicle_type']
            ))
            
            if len(batch) >= BATCH_SIZE:
                cursor.executemany(insert_query, batch)
                conn.commit()
                batch = []
        
        if batch:
            cursor.executemany(insert_query, batch)
            conn.commit()
        
        cursor.close()
        conn.close()
        logger.info(f"Successfully inserted all courier staff records from {csv_file}")
        
    except Error as e:
        logger.error(f"Error inserting courier staff: {e}")
        raise


def insert_routes(csv_file):
    """
    Insert route records from CSV file.
    
    Args:
        csv_file (str): Path to routes.csv
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        df = load_csv_file(csv_file)
        
        insert_query = """
            INSERT INTO routes 
            (route_id, origin, destination, distance_km, avg_time_hours)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE distance_km = VALUES(distance_km)
        """
        
        batch = []
        for i, row in df.iterrows():
            batch.append((
                row['route_id'],
                row['origin'],
                row['destination'],
                row['distance_km'],
                row['avg_time_hours']
            ))
            
            if len(batch) >= BATCH_SIZE:
                cursor.executemany(insert_query, batch)
                conn.commit()
                batch = []
        
        if batch:
            cursor.executemany(insert_query, batch)
            conn.commit()
        
        cursor.close()
        conn.close()
        logger.info(f"Successfully inserted all route records from {csv_file}")
        
    except Error as e:
        logger.error(f"Error inserting routes: {e}")
        raise


def insert_warehouses(json_file):
    """
    Insert warehouse records from JSON file.
    
    Args:
        json_file (str): Path to warehouses.json
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        data = load_json_file(json_file)
        
        insert_query = """
            INSERT INTO warehouses 
            (warehouse_id, city, state, capacity)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE capacity = VALUES(capacity)
        """
        
        batch = []
        for i, record in enumerate(data):
            batch.append((
                record.get('warehouse_id'),
                record.get('city'),
                record.get('state'),
                record.get('capacity')
            ))
            
            if len(batch) >= BATCH_SIZE:
                cursor.executemany(insert_query, batch)
                conn.commit()
                batch = []
        
        if batch:
            cursor.executemany(insert_query, batch)
            conn.commit()
        
        cursor.close()
        conn.close()
        logger.info(f"Successfully inserted all warehouse records from {json_file}")
        
    except Error as e:
        logger.error(f"Error inserting warehouses: {e}")
        raise


def insert_costs(csv_file):
    """
    Insert cost records from CSV file.
    
    Args:
        csv_file (str): Path to costs.csv
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        df = load_csv_file(csv_file)
        
        insert_query = """
            INSERT INTO costs 
            (shipment_id, fuel_cost, labor_cost, misc_cost)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE fuel_cost = VALUES(fuel_cost)
        """
        
        batch = []
        for i, row in df.iterrows():
            batch.append((
                row['shipment_id'],
                row['fuel_cost'],
                row['labor_cost'],
                row['misc_cost']
            ))
            
            if len(batch) >= BATCH_SIZE or i == len(df) - 1:
                cursor.executemany(insert_query, batch)
                conn.commit()
                logger.info(f"Inserted {len(batch)} cost records")
                batch = []
        
        cursor.close()
        conn.close()
        logger.info(f"Successfully inserted all cost records from {csv_file}")
        
    except Error as e:
        logger.error(f"Error inserting costs: {e}")
        raise


def ingest_all_data(base_path):
    """
    Ingest all logistics data from CSV and JSON files.
    
    Args:
        base_path (str): Base directory path containing all data files
    """
    try:
        logger.info("Starting data ingestion process...")
        
        # Insert in the correct order to avoid foreign key constraints
        insert_courier_staff(f"{base_path}/courier_staff.csv")
        insert_routes(f"{base_path}/routes.csv")
        insert_warehouses(f"{base_path}/warehouses.json")
        insert_shipments(f"{base_path}/shipments.json")
        insert_costs(f"{base_path}/costs.csv")
        insert_shipment_tracking(f"{base_path}/shipment_tracking.csv")
        
        logger.info("Data ingestion completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during data ingestion: {e}")
        raise


if __name__ == "__main__":
    # Run data ingestion
    base_path = "."  # Current directory
    ingest_all_data(base_path)
