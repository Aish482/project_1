# Smart Logistics Platform - Practical Usage Guide

## 📖 Common Scenarios & Solutions

This guide covers practical use cases and how to accomplish them using the platform.

---

## 1️⃣ Getting Started with the Dashboard

### Scenario: I just want to see what's in the database

**Steps:**
1. Run the application: `streamlit run app.py`
2. Go to **🏠 Home** page for overview
3. Click **📊 KPI Dashboard** to see summary metrics
4. Each metric is clickable for detailed information

**Expected Output:** High-level business metrics

---

## 2️⃣ Searching for Specific Information

### Scenario: Find a specific shipment by ID

**Steps:**
1. Navigate to **🔎 Shipment Search** page
2. Enter the shipment_id in the search box
3. Click **🔍 Search**
4. View full details and tracking history

**Example:**
```
Shipment ID: dc84cc15
Results: Shipment details, costs, tracking events
```

### Scenario: Find all cancelled shipments from a specific city

**Steps:**
1. Go to **🔎 Shipment Search** page
2. Set filters:
   - Status: "Cancelled"
   - Origin: Select desired city
3. Click **🔍 Apply Filters**
4. Review results and export if needed

---

## 3️⃣ Analyzing Performance

### Scenario: Which couriers are performing best?

**Steps:**
1. Navigate to **👥 Courier Performance**
2. Go to **On-Time Delivery** tab
3. Sort by `delivery_success_rate` (descending)
4. Filter by rating if needed

**Insights You'll Get:**
- Top performers by delivery rate
- Average delivery time per courier
- Relationship between rating and performance

### Scenario: Identify routes with delivery delays

**Steps:**
1. Go to **📈 Delivery Performance**
2. View **Most Delayed Routes** tab
3. Sort by `avg_delivery_days` (descending)
4. Compare with expected time from routes table

**Action Items:**
- Allocate more resources to delayed routes
- Investigate root causes
- Consider splitting high-traffic routes

---

## 4️⃣ Cost Optimization

### Scenario: Find shipments with unusually high costs

**Steps:**
1. Navigate to **💰 Cost Analytics**
2. Go to **High-Cost Shipments** tab
3. Review `cost_per_kg` column
4. Identify patterns (origin, destination, weight)

**Cost Breakdown Analysis:**
1. View **Fuel vs Labor** tab for cost distribution
2. Identify major cost drivers
3. Plan optimization strategies

### Scenario: Analyze costs by route

**Steps:**
1. **💰 Cost Analytics** → **Cost by Route** tab
2. Sort by `total_cost` (descending)
3. Compare with `distance_km` and `num_shipments`
4. Calculate cost efficiency

**Calculation:**
```
Cost per KM = total_cost / distance_km
Cost per Shipment = total_cost / num_shipments
```

---

## 5️⃣ Quality & Reliability Issues

### Scenario: High cancellation rates - find root cause

**Steps:**
1. Go to **❌ Cancellation Analysis**
2. Check **By Origin** tab → identify problem cities
3. Check **By Courier** tab → identify problem couriers
4. Cross-reference patterns

**Investigation Checklist:**
- [ ] Is it specific to certain couriers?
- [ ] Is it specific to certain origin cities?
- [ ] Is there a time pattern?
- [ ] Are certain routes more problematic?

### Scenario: Understand cancellation timeline

**Steps:**
1. **❌ Cancellation Analysis** → **Time to Cancellation** tab
2. Review `avg_days_to_cancel` column
3. Segment by origin-destination pair

**Actionable Insights:**
- Early cancellations → Payment/documentation issues
- Late cancellations → Delivery/route issues

---

## 6️⃣ Capacity & Resource Planning

### Scenario: Check warehouse utilization

**Steps:**
1. Go to **🏢 Warehouse Insights**
2. View **Capacity Comparison** tab
3. Sort by `utilization_rate` (descending)

**Analysis:**
- High utilization (>80%) → Consider expansion
- Low utilization (<30%) → Consider consolidation
- Medium (30-80%) → Optimal range

### Scenario: Identify high-traffic warehouses

**Steps:**
1. **🏢 Warehouse Insights** → **High-Traffic Warehouses**
2. Review `num_shipments` and `num_couriers`
3. Compare with warehouse capacity

---

## 7️⃣ Data Export & Reporting

### Export Performance Report

**Using Python Script:**
```python
from utils import DataExportManager, LogisticsAnalytics

# Export KPI report
report = LogisticsAnalytics.generate_performance_report(days=30)

# Export to CSV
top_couriers = LogisticsQueries.get_courier_performance()
DataExportManager.export_to_csv(top_couriers, 'top_couriers.csv')

# Export to Excel
DataExportManager.export_to_excel(top_couriers, 'performance.xlsx')
```

### Generate Custom Report

```python
from streamlit import dataframe
from queries import LogisticsQueries

# Get data
delayed_routes = LogisticsQueries.get_most_delayed_routes()

# Display or export
dataframe(delayed_routes)
```

---

## 8️⃣ Advanced Analytics

### Identifying Performance Bottlenecks

**Steps:**
```python
from utils import LogisticsAnalytics

# Identify routes with delays > 75th percentile
bottlenecks = LogisticsAnalytics.identify_bottleneck_routes(threshold_percentile=75)
print(f"Found {len(bottlenecks)} bottleneck routes")
print(bottlenecks[['origin', 'destination', 'avg_delivery_days']])
```

### Cost Pattern Analysis

**Steps:**
```python
from utils import LogisticsAnalytics

# Comprehensive cost analysis
analysis = LogisticsAnalytics.analyze_cost_patterns()

print("High-cost routes:")
print(analysis['high_cost_routes'])

print("\nCost breakdown (%):")
print(analysis['cost_breakdown'])
```

### Quality Assurance

**Steps:**
```python
from utils import DataQualityChecker

# Check for data issues
issues = DataQualityChecker.validate_data_consistency()
print(f"Orphaned tracking records: {issues['orphaned_tracking']}")
print(f"Invalid courier references: {issues['invalid_couriers']}")
```

---

## 9️⃣ Dashboarding Best Practices

### Daily Operations Checklist

1. **Morning Standup** (5 min)
   - View KPI Dashboard
   - Check for any critical issues
   - Review overnight shipments

2. **Route Optimization** (15 min)
   - Check Most Delayed Routes
   - Identify bottlenecks
   - Allocate resources

3. **Cost Review** (10 min)
   - Verify cost trends
   - Check high-cost shipments
   - Monitor fuel vs labor split

4. **Courier Performance** (10 min)
   - Review delivery rates
   - Identify top/low performers
   - Plan training if needed

### Weekly Review (30 min)

1. Generate performance report
   ```python
   from utils import LogisticsAnalytics
   weekly_report = LogisticsAnalytics.generate_performance_report(days=7)
   ```

2. Compare week-over-week metrics
3. Identify trends
4. Plan interventions

### Monthly Strategy

1. Review all analytical views
2. Identify top/bottom performers
3. Plan optimization initiatives
4. Budget review based on costs
5. Capacity planning

---

## 🔟 Quick Queries (for technical users)

### Top 10 Couriers by Shipments
```python
from queries import LogisticsQueries
df = LogisticsQueries.get_courier_performance()
print(df.nlargest(10, 'num_shipments')[['name', 'num_shipments', 'delivery_rate']])
```

### Cost Breakdown
```python
from queries import LogisticsQueries
breakdown = LogisticsQueries.get_fuel_vs_labor_contribution()
print(breakdown)
```

### Shipment Tracking
```python
from queries import LogisticsQueries
tracking = LogisticsQueries.get_shipment_tracking_history('dc84cc15')
print(tracking)
```

### Filter Shipments
```python
from queries import LogisticsQueries
results = LogisticsQueries.filter_shipments(
    status='Delivered',
    origin='New York',
    start_date='2025-06-01'
)
print(f"Found {len(results)} delivered shipments")
```

---

## 1️⃣1️⃣ Troubleshooting Common Issues

### Issue: "No data showing in charts"

**Solutions:**
1. Click "Initialize Database" in sidebar
2. Click "Load Data" to import CSV/JSON files
3. Wait for data to fully load (3-4 minutes for 350K records)
4. Refresh browser (F5)

### Issue: "Slow dashboard response"

**Solutions:**
1. Clear browser cache
2. Try filtering data before viewing
3. Check database performance:
   ```python
   from utils import PerformanceTuning
   stats = PerformanceTuning.get_table_statistics()
   print(stats)
   ```

### Issue: "Filters not working"

**Solutions:**
1. Make sure data is loaded
2. Try resetting filters
3. Reload the page
4. Check browser console for errors

---

## 1️⃣2️⃣ Advanced Use Cases

### Real-time Monitoring Setup

```python
import time
from queries import LogisticsQueries
import streamlit as st

# Refresh KPIs every 5 minutes
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active Shipments", len(LogisticsQueries.filter_shipments(status='In Transit')))

with col2:
    st.metric("Delivery Rate", f"{LogisticsQueries.get_delivered_percentage():.1f}%")

with col3:
    st.metric("Avg Cost", f"${LogisticsQueries.get_total_operational_cost() / LogisticsQueries.get_total_shipments():.2f}")

# Auto-refresh every 5 minutes
time.sleep(300)
st.rerun()
```

### Predictive Alerts

```python
from utils import LogisticsAnalytics

# Identify problematic shipments
issues = LogisticsAnalytics.predict_problematic_shipments()

if len(issues) > 0:
    st.warning(f"⚠️ {len(issues)} couriers with high cancellation rates detected!")
    st.dataframe(issues)
```

---

## 📚 Additional Resources

- [Database Schema](README.md#-database-schema)
- [Installation Guide](SETUP_GUIDE.md)
- [Query Reference](queries.py)
- [Streamlit Documentation](https://docs.streamlit.io)

---

## 💡 Tips for Maximum Effectiveness

1. **Use Filters** - Always filter data by relevant criteria
2. **Export Reports** - Build historical trend analysis
3. **Set Alerts** - Monitor problematic routes/couriers
4. **Benchmark** - Compare against previous periods
5. **Document Issues** - Keep notes on action items
6. **Regular Reviews** - Schedule weekly/monthly reports
7. **Test Changes** - Track impact of optimizations

---

**Last Updated:** February 2026  
**Platform Version:** 1.0 ✅
