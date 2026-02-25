"""
Setup and initialization script for the Logistics Analytics Platform.
Run this once to set up the database schema and load initial data.
"""

import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_project():
    """
    Complete setup workflow for the project.
    """
    print("\n" + "="*60)
    print("🚀 Smart Logistics Management & Analytics Platform")
    print("📦 Project Setup Wizard")
    print("="*60 + "\n")
    
    try:
        # Step 1: Database Initialization
        print("Step 1: Initializing Database Schema...")
        from database import create_tables, drop_all_tables
        
        reset = input("Do you want to reset existing tables? (yes/no): ").lower()
        if reset == 'yes':
            print("Dropping existing tables...")
            drop_all_tables()
            print("✅ Tables dropped successfully")
        
        print("Creating new tables...")
        create_tables()
        print("✅ Database schema created successfully\n")
        
        # Step 2: Data Ingestion
        print("Step 2: Loading Data from Files...")
        from data_ingestion import ingest_all_data
        
        load_data = input("Do you want to load data from CSV/JSON files? (yes/no): ").lower()
        if load_data == 'yes':
            base_path = input("Enter base path for data files (default: current directory): ").strip()
            if not base_path:
                base_path = "."
            
            print(f"Loading data from {base_path}...")
            ingest_all_data(base_path)
            print("✅ Data loaded successfully\n")
        
        # Step 3: Verification
        print("Step 3: Verifying Data...")
        from queries import LogisticsQueries
        
        try:
            total = LogisticsQueries.get_total_shipments()
            print(f"✅ Verified: {total:,} shipments in database\n")
        except Exception as e:
            print(f"⚠️ Verification warning: {e}\n")
        
        # Step 4: Summary
        print("="*60)
        print("✅ Setup Completed Successfully!")
        print("="*60)
        print("\nNext Steps:")
        print("1. Run the Streamlit app:")
        print("   streamlit run app.py")
        print("\n2. Open your browser to http://localhost:8501")
        print("\n3. Navigate through the dashboard to explore analytics")
        print("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        print(f"\n❌ Setup Error: {e}")
        sys.exit(1)


def test_connections():
    """
    Test database connectivity and data availability.
    """
    print("\n" + "="*60)
    print("🔧 Testing System Connections")
    print("="*60 + "\n")
    
    try:
        from database import get_connection
        
        print("Testing MySQL connection...")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'logistic'")
        table_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ MySQL Connection: OK ({table_count} tables found)")
        
        from queries import LogisticsQueries
        
        total_shipments = LogisticsQueries.get_total_shipments()
        delivered_pct = LogisticsQueries.get_delivered_percentage()
        
        print(f"✅ Query Execution: OK")
        print(f"   - Total Shipments: {total_shipments:,}")
        print(f"   - Delivered %: {delivered_pct or 0:.1f}%")
        
        print("\n" + "="*60)
        print("✅ All tests passed! Ready to use.")
        print("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        print(f"\n❌ Test Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup script for Logistics Analytics Platform")
    parser.add_argument('--setup', action='store_true', help='Run complete setup wizard')
    parser.add_argument('--test', action='store_true', help='Test database connections')
    parser.add_argument('--all', action='store_true', help='Run setup and tests')
    
    args = parser.parse_args()
    
    if args.setup or args.all:
        setup_project()
    
    if args.test or args.all:
        test_connections()
    
    if not any([args.setup, args.test, args.all]):
        print("Usage: python setup.py --setup | --test | --all")
        print("\nrun: python setup.py --all")
