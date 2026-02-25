# project_1
Smart Logistics Management &amp; Analytics Platform



This project aims to build a centralized Smart Logistics Management and Analytics Platform that consolidates operational data into a MySQL database and provides an interactive Streamlit dashboard for real-time analysis and decision-making.

2️⃣ Project Objective
The objective of this project is to design and implement an end-to-end logistics analytics system that:
Ingests large-scale logistics datasets (70,000+ shipment records).


Stores data in a normalized MySQL relational database.


Enables shipment-level tracking through status logs.


Provides operational insights via Streamlit dashboards.


Supports filtering, KPI monitoring, and business performance evaluation.



3️⃣ Data Architecture Overview
The system integrates structured data across six core datasets:
Shipments


Shipment Tracking


Courier Staff


Routes


Warehouses


Costs


These datasets simulate real-world logistics operations.

4️⃣ Database Schema (MySQL)

DATASET LINK - Logistics_dataset
Complete Table Schema with Column Descriptions
📦 Table: shipments
Column Name
Data Type
Description
shipment_id
VARCHAR(50) PRIMARY KEY
Unique identifier for each shipment/order
order_date
DATE
Date when the shipment order was created
origin
VARCHAR(100)
City/location where shipment starts
destination
VARCHAR(100)
Delivery city/location
weight
DECIMAL(10,2)
Weight of the shipment in kg
courier_id
VARCHAR(50)
Courier responsible for delivery (FK to courier_staff)
status
VARCHAR(50)
Current shipment status (Delivered, In Transit, Cancelled, etc.)
delivery_date
DATE NULL
Date when shipment was delivered (NULL if not delivered yet)


 Table: shipment_tracking
Column Name
Data Type
Description
tracking_id
INT PRIMARY KEY
Unique identifier for tracking event
shipment_id
VARCHAR(50)
Shipment linked to this event (FK to shipments)
status
VARCHAR(50)
Status update at this stage (Picked Up, In Transit, Delivered, etc.)
timestamp
DATETIME
Date & time when this tracking event occurred

Table: courier_staff
Column Name
Data Type
Description
courier_id
VARCHAR(50) PRIMARY KEY
Unique identifier for courier employee
name
VARCHAR(150)
Full name of courier
rating
DECIMAL(3,1)
Courier performance rating (1–5 scale)
vehicle_type
VARCHAR(50)
Type of delivery vehicle used (Bike, Van, Truck, Car)

Table: routes
Column Name
Data Type
Description
route_id
VARCHAR(50) PRIMARY KEY
Unique identifier for transport route
origin
VARCHAR(100)
Starting city/location of route
destination
VARCHAR(100)
Ending city/location of route
distance_km
DECIMAL(10,2)
Distance between origin and destination in kilometers
avg_time_hours
DECIMAL(5,2)
Average travel time expected for this route


Table: warehouses
Column Name
Data Type
Description
warehouse_id
VARCHAR(50) PRIMARY KEY
Unique identifier for warehouse
city
VARCHAR(100)
City where warehouse is located
state
VARCHAR(50)
State or region of warehouse
capacity
INT
Maximum shipment capacity warehouse can handle


Table: costs
Column Name
Data Type
Description
shipment_id
VARCHAR(50) PRIMARY KEY
Shipment linked to cost record (FK to shipments)
fuel_cost
DECIMAL(15,2)
Fuel cost incurred for shipment delivery
labor_cost
DECIMAL(15,2)
Courier labor cost for shipment
misc_cost
DECIMAL(15,2)
Additional operational costs (handling, packaging, etc.)

5️⃣ System Workflow
Import CSV/JSON datasets into MySQL.


Establish foreign key relationships.


Build optimized SQL queries for KPIs.


Connect Streamlit to MySQL using a Python database connector.


Display real-time data with filtering options.



6️⃣ Streamlit Dashboard Features
The Streamlit interface will include:

🔎 A. Shipment Search & Filtering
Search by shipment_id


Filter by:


Status (Delivered, Cancelled, In Transit)


Origin / Destination


Date range


Courier



📊 B. Operational KPIs
Total Shipments


Delivered Shipments %


Cancelled Shipments %


Average Delivery Time


Total Operational Cost



📈 C. Analytical Views
1️⃣ Delivery Performance Insights
Average delivery time per route


Most delayed routes


Delivery time vs distance comparison


2️⃣ Courier Performance
Shipments handled per courier


On-time delivery %


Average rating comparison


3️⃣ Cost Analytics
Total cost per shipment


Cost per route


Fuel vs labor percentage contribution


High-cost shipments


4️⃣ Cancellation Analysis
Cancellation rate by origin


Cancellation rate by courier


Time-to-cancellation analysis


5️⃣ Warehouse Insights
Warehouse capacity comparison


High-traffic warehouse cities

