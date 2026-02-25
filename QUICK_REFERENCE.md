# 📋 Smart Logistics Platform - Quick Reference

## ⚡ Quick Start Commands

### Windows
```bash
# First time setup
run.bat --setup

# Regular start
run.bat
```

### Linux/Mac
```bash
# First time setup
./run.sh --setup

# Regular start
./run.sh
```

### Manual Start
```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Initialize database
python setup.py --setup

# Run tests
python setup.py --test

# Start dashboard
streamlit run app.py
```

---

## 🗄️ Database Commands

### Connect to MySQL
```bash
mysql -h localhost -u root -p logistic
```

### View Tables
```sql
SHOW TABLES;
```

### Check Data Counts
```sql
SELECT 'shipments' as table_name, COUNT(*) as count FROM shipments
UNION
SELECT 'courier_staff', COUNT(*) FROM courier_staff
UNION
SELECT 'routes', COUNT(*) FROM routes
UNION
SELECT 'warehouses', COUNT(*) FROM warehouses
UNION
SELECT 'costs', COUNT(*) FROM costs
UNION
SELECT 'shipment_tracking', COUNT(*) FROM shipment_tracking;
```

### Reset Database
```python
python -c "from database import drop_all_tables, create_tables; drop_all_tables(); create_tables()"
```

---

## 📊 Dashboard Navigation

| Page | Purpose | Key Metrics |
|------|---------|------------|
| 🏠 Home | Overview | Project info |
| 📊 KPIs | Executive summary | 5 key metrics |
| 📈 Delivery | Route analysis | Performance vs distance |
| 👥 Couriers | Team performance | Ratings, delivery rate |
| 💰 Costs | Budget optimization | Fuel vs labor |
| ❌ Cancellations | Quality issues | Cancellation rates |
| 🏢 Warehouses | Capacity planning | Utilization rates |
| 🔎 Search | Find shipments | Filter & track |

---

## 🔍 Common Python Queries

### Get Total Shipments
```python
from queries import LogisticsQueries
total = LogisticsQueries.get_total_shipments()
```

### Get Top Couriers
```python
couriers = LogisticsQueries.get_courier_performance()
top_10 = couriers.nlargest(10, 'num_shipments')
```

### Find Shipment
```python
shipment = LogisticsQueries.search_shipment('dc84cc15')
```

### Get Tracking History
```python
tracking = LogisticsQueries.get_shipment_tracking_history('dc84cc15')
```

### Filter Shipments
```python
results = LogisticsQueries.filter_shipments(
    status='Delivered',
    origin='New York'
)
```

### Export Data
```python
from utils import DataExportManager
DataExportManager.export_to_csv(results, 'export.csv')
```

---

## 🎯 Key Performance Indicators

| KPI | Formula | Insight |
|-----|---------|---------|
| Delivery Rate | (Delivered / Total) × 100 | % of on-time deliveries |
| Cancellation Rate | (Cancelled / Total) × 100 | % of cancelled shipments |
| Avg Delivery Time | AVG(delivery_date - order_date) | Days to deliver |
| Cost per Shipment | Total Cost / Total Shipments | Average cost |
| Cost per KG | Total Cost / Total Weight | Pricing metric |
| Courier Rating | AVG(rating) by courier | Performance 1-5 |
| Utilization Rate | (Shipments / Capacity) × 100 | Warehouse usage |
| Route Efficiency | Actual Time / Expected Time | Time performance |

---

## 📈 Common Analysis Patterns

### Performance by Courier
```python
perf = LogisticsQueries.get_courier_performance()
perf.sort_values('delivery_rate', ascending=False)
```

### Cost Analysis
```python
costs = LogisticsQueries.get_cost_per_route()
costs.sort_values('total_cost', ascending=False).head(10)
```

### Route Delays
```python
delays = LogisticsQueries.get_most_delayed_routes()
delays[delays['avg_delivery_days'] > delays['avg_delivery_days'].mean()]
```

### Cancellation Patterns
```python
cancel = LogisticsQueries.get_cancellation_rate_by_origin()
cancel[cancel['cancellation_rate'] > 10]
```

---

## 🚨 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| MySQL not connecting | Start MySQL service, check credentials |
| No data showing | Run "Load Data", wait 3-4 minutes |
| Slow dashboard | Clear cache, filter data first |
| Port 8501 in use | Use `streamlit run app.py --server.port 8502` |
| Module not found | Activate venv, reinstall requirements |
| Database error | Drop/recreate: `python setup.py --all` |

---

## 📁 File Locations

```
projects/datasets/
├── app.py                 ← Main dashboard
├── database.py            ← DB connection
├── data_ingestion.py      ← Load data
├── queries.py             ← SQL queries
├── utils.py               ← Helper functions
├── setup.py               ← Setup wizard
├── README.md              ← Documentation
├── SETUP_GUIDE.md         ← Installation
├── USAGE_GUIDE.md         ← How to use
├── QUICK_REFERENCE.md     ← This file
├── requirements.txt       ← Python packages
├── shipments.json         ← 70K shipments
├── shipment_tracking.csv  ← 209K tracking
├── courier_staff.csv      ← 1K couriers
├── routes.csv             ← 500 routes
├── warehouses.json        ← 300 warehouses
└── costs.csv              ← 70K costs
```

---

## 🔑 Database Credentials

```
Host: localhost
Port: 3306
Username: root
Password: #Bb.5121
Database: logistic
```

⚠️ **Remember:** Never hardcode credentials in production!

---

## 🌐 Web URLs

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:8501 |
| MySQL | localhost:3306 |
| Streamlit Docs | https://docs.streamlit.io |
| MySQL Docs | https://dev.mysql.com/doc |

---

## 📞 Support Channels

### Check Database
```bash
mysql -h localhost -u root -p -e "SELECT COUNT(*) FROM logistic.shipments;"
```

### Check Python
```bash
python --version
pip list | grep streamlit
```

### View Application Logs
```bash
streamlit logs
```

### Test Connection
```python
python -c "from database import get_connection; con = get_connection(); print('OK')"
```

---

## ✅ Pre-Flight Checklist

Before starting:
- [ ] MySQL is running
- [ ] All CSV/JSON files present
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Requirements installed
- [ ] Database initialized
- [ ] Data loaded

---

## 🎓 Learning Resources

| Topic | Resource |
|-------|----------|
| Streamlit | https://docs.streamlit.io/library/api-reference |
| MySQL | https://dev.mysql.com/doc/refman/5.7/en |
| Pandas | https://pandas.pydata.org/docs |
| Plotly | https://plotly.com/python |
| Python | https://docs.python.org/3 |

---

## 🔄 Typical Workflows

### Monday Morning - Week Review
```python
from utils import LogisticsAnalytics
report = LogisticsAnalytics.generate_performance_report(days=7)
# Review KPIs from last week
```

### Daily - Performance Check
```python
from queries import LogisticsQueries
kpis = {
    'total': LogisticsQueries.get_total_shipments(),
    'delivered': LogisticsQueries.get_delivered_percentage(),
    'cost': LogisticsQueries.get_total_operational_cost()
}
```

### Weekly - Cost Review
```python
from queries import LogisticsQueries
costs = LogisticsQueries.get_cost_per_route()
high_cost = costs.nlargest(10, 'total_cost')
```

---

## 💡 Pro Tips

1. **Bookmarks** - Save dashboard pages for quick access
2. **Filters** - Always filter by date range for speed
3. **Export** - Download reports for archiving
4. **Alerts** - Monitor cancellation rates
5. **Trends** - Compare week-to-week metrics
6. **Notes** - Document action items
7. **Backup** - Regular database backups

---

## 📊 Sample SQL Queries

### High-Cost Shipments
```sql
SELECT shipment_id, 
       fuel_cost + labor_cost + misc_cost as total_cost
FROM costs
ORDER BY total_cost DESC
LIMIT 20;
```

### Delivery Performance by Courier
```sql
SELECT c.name,
       COUNT(s.shipment_id) as shipments,
       AVG(DATEDIFF(s.delivery_date, s.order_date)) as avg_days
FROM courier_staff c
JOIN shipments s ON c.courier_id = s.courier_id
WHERE s.status = 'Delivered'
GROUP BY c.courier_id, c.name
ORDER BY avg_days ASC;
```

### Route Analysis
```sql
SELECT s.origin, s.destination,
       COUNT(s.shipment_id) as num_shipments,
       AVG(DATEDIFF(s.delivery_date, s.order_date)) as avg_days,
       r.distance_km
FROM shipments s
LEFT JOIN routes r ON s.origin = r.origin AND s.destination = r.destination
GROUP BY s.origin, s.destination
ORDER BY num_shipments DESC;
```

---

## 🎯 30-Day Implementation Plan

### Week 1: Setup
- Day 1: Install Python, MySQL, requirements
- Day 2: Initialize database, load data
- Day 3: Explore dashboard, understand data
- Day 4-7: Run through all views, identify issues

### Week 2: Analysis
- Day 8-10: Deep dive into courier performance
- Day 11-12: Cost analysis and optimization
- Day 13-14: Route efficiency review

### Week 3: Optimization
- Day 15-17: Implement improvements
- Day 18-19: Track impact of changes
- Day 20-21: Report on ROI

### Week 4: Production
- Day 22-26: Fine-tune and optimize
- Day 27-28: Staff training
- Day 29-30: Go live and monitor

---

**Last Updated:** February 2026  
**Platform Version:** 1.0 ✅  
**Status:** Production Ready
