**Note: **Make sure to set DB password accordingly for database.py(check schema as well) and readme.md and then execute .\run.bat to view Streamlit logistic dashboard.



# Smart Logistics Management & Analytics Platform

## 📋 Project Overview

A comprehensive end-to-end logistics analytics system that consolidates operational data from multiple sources into a centralized MySQL database and provides an interactive Streamlit dashboard for real-time analysis and decision-making.

**Key Features:**
- 70,000+ shipment records management
- Real-time shipment tracking
- Operational KPI monitoring
- Performance benchmarking
- Cost transparency and analysis
- Actionable logistics insights

## 🎯 Project Objectives

✅ Ingest large-scale logistics datasets (70,000+ shipment records)
✅ Store data in a normalized MySQL relational database
✅ Enable shipment-level tracking through status logs
✅ Provide operational insights via Streamlit dashboards
✅ Support filtering, KPI monitoring, and business performance evaluation

## 📊 Data Architecture

### Core Datasets (6 tables)

1. **Shipments** (70,000+ records)
   - Shipment details, origin, destination, weight, status
   - Courier assignment and delivery dates

2. **Shipment Tracking** (209,000+ records)
   - Real-time tracking events with timestamps
   - Status updates throughout delivery lifecycle

3. **Courier Staff** (1,000+ records)
   - Courier information, ratings, vehicle types

4. **Routes** (500+ records)
   - Route details, distance, average travel time

5. **Warehouses** (300+ records)
   - Warehouse locations, capacity, utilization

6. **Costs** (70,000+ records)
   - Fuel, labor, and miscellaneous costs per shipment

## 🗄️ Database Schema

### MySQL Tables Structure

```sql
-- Shipments Table
shipment_id (VARCHAR 50, PK)
order_date (DATE)
origin (VARCHAR 100)
destination (VARCHAR 100)
weight (DECIMAL 10,2)
courier_id (VARCHAR 50, FK)
status (VARCHAR 50)
delivery_date (DATE, NULL)

-- Shipment Tracking Table
tracking_id (INT, PK, AUTO_INCREMENT)
shipment_id (VARCHAR 50, FK)
status (VARCHAR 50)
timestamp (DATETIME)

-- Courier Staff Table
courier_id (VARCHAR 50, PK)
name (VARCHAR 150)
rating (DECIMAL 3,1)
vehicle_type (VARCHAR 50)

-- Routes Table
route_id (VARCHAR 50, PK)
origin (VARCHAR 100)
destination (VARCHAR 100)
distance_km (DECIMAL 10,2)
avg_time_hours (DECIMAL 5,2)

-- Warehouses Table
warehouse_id (VARCHAR 50, PK)
city (VARCHAR 100)
state (VARCHAR 50)
capacity (INT)

-- Costs Table
shipment_id (VARCHAR 50, PK, FK)
fuel_cost (DECIMAL 15,2)
labor_cost (DECIMAL 15,2)
misc_cost (DECIMAL 15,2)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL Server running locally
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd e:\projects\datasets
   ```

2. **Install required packages**
   ```bash
   pip install streamlit mysql-connector-python pandas plotly
   ```

3. **Update database credentials (if needed)**
   Edit credentials in `database.py`:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': 'your_password',
       'database': 'logistic'
   }
   ```

### Quick Start

1. **Initialize the database**
   ```bash
   python database.py
   ```

2. **Load data into MySQL**
   ```bash
   python data_ingestion.py
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

4. Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
├── app.py                    # Main Streamlit dashboard application
├── database.py              # Database connection and schema management
├── data_ingestion.py        # CSV/JSON data loading and insertion
├── queries.py               # SQL queries for analytics and KPIs
├── README.md                # Project documentation
├── shipments.json           # Shipment data (70,000+ records)
├── shipment_tracking.csv    # Tracking events (209,000+ records)
├── courier_staff.csv        # Courier information (1,000+ records)
├── routes.csv               # Route details (500+ records)
├── warehouses.json          # Warehouse data (300+ records)
└── costs.csv                # Cost data (70,000+ records)
```

## 🎨 Dashboard Features

### 🏠 Home Page
- Project overview and quick start guide
- System architecture overview

### 📊 KPI Dashboard
- Total Shipments
- Delivered Shipments %
- Cancelled Shipments %
- Average Delivery Time
- Total Operational Cost

### 📈 Delivery Performance
- Average delivery time per route
- Most delayed routes
- Delivery time vs distance analysis
- Route efficiency metrics

### 👥 Courier Performance
- Shipments handled per courier
- On-time delivery percentages
- Courier rating comparison
- Performance rankings

### 💰 Cost Analytics
- High-cost shipments
- Cost per route analysis
- Fuel vs labor cost breakdown
- Cost per kilogram metrics
- Cost optimization insights

### ❌ Cancellation Analysis
- Cancellation rate by origin
- Cancellation rate by courier
- Time-to-cancellation analysis
- Pattern identification

### 🏢 Warehouse Insights
- Warehouse capacity comparison
- Utilization rates
- High-traffic warehouses
- Capacity planning

### 🔎 Shipment Search & Filtering
- Search by Shipment ID
- Filter by:
  - Status (Delivered, Cancelled, In Transit)
  - Origin/Destination cities
  - Date range
  - Courier
- Tracking history visualization

## 🔑 Key SQL Queries

### Operational KPIs
- Total shipments count
- Delivery percentage
- Cancellation percentage
- Average delivery time
- Total operational cost

### Performance Metrics
- Average delivery time per route
- Most delayed routes
- Courier performance rankings
- On-time delivery rates

### Cost Analysis
- Cost per shipment
- Cost by route
- Fuel vs labor contribution
- High-cost shipments

### Business Insights
- Cancellation patterns
- Warehouse utilization
- Route efficiency
- Courier reliability

## 💡 Business Insights

This system helps answer critical business questions:

- **Which routes have the highest delays?**
- **Which couriers handle most shipments?**
- **Are high-rated couriers delivering faster?**
- **Which shipments are most expensive?**
- **Is cost directly proportional to weight?**
- **Which cities generate maximum cancellations?**
- **Which routes are underperforming relative to distance?**
- **What's the warehouse utilization rate?**
- **How much fuel vs labor contributes to costs?**

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.8+ |
| **Database** | MySQL/MariaDB |
| **Backend** | MySQL Connector |
| **Frontend** | Streamlit |
| **Data Processing** | Pandas |
| **Visualization** | Plotly |
| **Data Formats** | CSV, JSON |

## 📈 Data Processing Pipeline

```
┌─────────────────┐
│  Source Data    │
│ (CSV/JSON)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Validation   │
│   & Parsing     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Batch Insert   │
│  to MySQL       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Streamlit     │
│   Dashboard     │
└─────────────────┘
```

## ⚙️ Configuration

### Database Connection
Edit credentials in `database.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'logistic'
}
```

### Batch Size for Data Loading
In `data_ingestion.py`:
```python
BATCH_SIZE = 500  # Adjust for performance
```

## 🔍 Usage Guide

### Initializing the System

1. **Start MySQL Server**
   - Ensure MySQL is running on localhost

2. **Initialize Database**
   - Click "Initialize Database" in the Streamlit sidebar
   - Optional: Click "Load Data" to import all CSV/JSON files

### Using the Dashboard

1. **View KPIs** - Go to KPI Dashboard page for overview metrics

2. **Analyze Performance** - Visit Delivery Performance to identify bottlenecks

3. **Track Couriers** - Check Courier Performance for efficiency metrics

4. **Optimize Costs** - Review Cost Analytics for cost-saving opportunities

5. **Search Shipments** - Use Shipment Search to find specific orders

## 🐛 Error Handling

The system includes comprehensive error handling:
- Database connection errors
- Data validation errors
- Query execution errors
- File loading errors

All errors are logged and displayed in the UI.

## 📊 Performance Optimization

- **Indexes**: Added on frequently queried columns (status, courier_id, dates)
- **Batch Processing**: Data inserted in batches for speed
- **Query Optimization**: Efficient joins and aggregations
- **Pagination**: Limits on result sets to prevent memory overload

## 🔐 Best Practices Implemented

✅ PEP 8 Python formatting
✅ Descriptive variable and function names
✅ Modular code structure
✅ Comprehensive docstrings
✅ Error handling with try-except
✅ Logging for debugging
✅ Database normalization
✅ Foreign key relationships
✅ Query indexing
✅ Batch processing for performance

## 📝 Data Quality Assurance

- Input validation on all data loads
- Duplicate handling with ON DUPLICATE KEY UPDATE
- NULL value management for nullable fields
- Data type consistency
- Referential integrity through foreign keys

## 🚢 Deployment Considerations

- Use environment variables for credentials
- Implement connection pooling for production
- Add authentication to Streamlit app
- Use persistent database backups
- Monitor query performance with EXPLAIN
- Set up database replication for redundancy

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- Weekly database backups
- Monthly query performance analysis
- Quarterly schema optimization
- Annual capacity planning

### Troubleshooting

**Issue: Database connection failed**
- Verify MySQL service is running
- Check credentials in database.py
- Ensure database 'logistic' exists

**Issue: Data not loading**
- Verify CSV/JSON files are in the same directory
- Check file format and encoding
- Review logs for specific errors

**Issue: Slow dashboard performance**
- Check query logs with EXPLAIN
- Verify indexes are created
- Reduce data range in filters

## 📚 References

- [Streamlit Documentation](https://docs.streamlit.io)
- [MySQL Documentation](https://dev.mysql.com/doc)
- [Pandas Documentation](https://pandas.pydata.org/docs)
- [Plotly Documentation](https://plotly.com/python)

## 🎓 Skills Demonstrated

✅ **Python Scripting** - Data processing and application logic
✅ **SQL Database Management** - Schema design and query optimization
✅ **Data Extraction** - JSON parsing and CSV handling
✅ **Data Analysis** - Complex queries and KPI calculations
✅ **Web Application Development** - Streamlit dashboard creation
✅ **Software Engineering** - Modular design and error handling

## 📄 License

This project is provided as-is for educational and business analytics purposes.

## 👨‍💻 Author

Developed as a Smart Logistics Management & Analytics Platform capstone project.

---

**Last Updated**: February 2026
**Version**: 1.0
**Status**: Production Ready ✅


