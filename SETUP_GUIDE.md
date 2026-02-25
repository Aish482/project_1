# Smart Logistics Platform - Setup & Installation Guide

## 📋 Quick Reference

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.8+ | Required |
| MySQL | 5.7+ | Required |
| Streamlit | 1.28.1 | Included |
| Pandas | 2.0.3 | Included |
| Plotly | 5.17.0 | Included |

## 🔧 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] MySQL Server installed and running
- [ ] MySQL user with database creation privileges
- [ ] pip (Python package manager)
- [ ] Git (optional, for version control)

### Verify Installation

**Check Python:**
```bash
python --version
# Should show Python 3.8 or higher
```

**Check MySQL:**
```bash
mysql --version
# Should show MySQL version
```

## 💻 Installation Steps

### Step 1: Prepare MySQL Database

#### Option A: Using MySQL Command Line

1. **Open MySQL Command Shell**
   ```bash
   mysql -u root -p
   # Enter your MySQL root password
   ```

2. **Create Database**
   ```sql
   CREATE DATABASE logistic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;
   ```

#### Option B: Using MySQL Workbench or GUI Tool

1. Connect to your MySQL server
2. Create new schema named `logistic`
3. Set character set to `utf8mb4`

### Step 2: Download & Setup Project

1. **Clone or Download the Project**
   ```bash
   # Option 1: Clone from GitHub (if available)
   git clone <repository-url>
   cd projects/datasets
   
   # Option 2: Manual download
   # Download and extract the project folder
   ```

2. **Navigate to Project Directory**
   ```bash
   cd e:\projects\datasets
   ```

### Step 3: Configure Database Connection

Edit `database.py` and verify/update the connection parameters:

```python
DB_CONFIG = {
    'host': 'localhost',        # MySQL host
    'user': 'root',             # MySQL username
    'password': '#Bb.5121',     # MySQL password
    'database': 'logistic'      # Database name
}
```

**Important:** Never hardcode credentials in production. Use environment variables:

```python
# Alternative: Using environment variables
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'logistic')
}
```

### Step 4: Install Python Dependencies

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Verify Data Files

Ensure all data files are in the project directory:

```bash
✓ shipments.json           (70,000+ shipment records)
✓ shipment_tracking.csv    (209,000+ tracking events)
✓ courier_staff.csv        (1,000+ courier records)
✓ routes.csv               (500+ route records)
✓ warehouses.json          (300+ warehouse records)
✓ costs.csv                (70,000+ cost records)
```

## 🚀 Running the Application

### Quick Start (Recommended)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

### Manual Start

1. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Run Setup (First Time)**
   ```bash
   python setup.py --all
   ```
   
   This will:
   - Initialize database schema
   - Load all data from CSV/JSON files
   - Verify connections and data

3. **Start Streamlit App**
   ```bash
   streamlit run app.py
   ```

4. **Open in Browser**
   - Browser should open automatically to `http://localhost:8501`
   - If not, manually open the URL

## 📊 Dashboard Initialization

When you first open the dashboard:

1. **Click "🔧 Initialize Database"** in the sidebar
   - Creates all required tables
   - Sets up indexes and relationships

2. **Click "📥 Load Data"** in the sidebar
   - Imports all CSV and JSON files
   - Inserts data into database tables
   - Displays progress

3. **Start Exploring**
   - Navigate through different analytics pages
   - Search for specific shipments
   - Apply filters and view reports

## 🔍 Troubleshooting

### Issue: "MySQL Connection Error"

**Solution:**
1. Verify MySQL server is running
2. Check credentials in `database.py`
3. Ensure database `logistic` exists
4. Test connection:
   ```bash
   mysql -h localhost -u root -p -e "SHOW DATABASES;"
   ```

### Issue: "ModuleNotFoundError"

**Solution:**
1. Verify virtual environment is activated
2. Reinstall requirements:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Issue: "Data file not found"

**Solution:**
1. Verify CSV/JSON files are in project directory
2. Check file names match exactly (case-sensitive on Linux/Mac)
3. Verify file permissions (readable)

### Issue: "Streamlit not opening in browser"

**Solution:**
1. Manually open `http://localhost:8501` in browser
2. Check firewall isn't blocking port 8501
3. Try different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```

### Issue: "Slow dashboard performance"

**Solution:**
1. Clear Streamlit cache:
   ```bash
   streamlit cache clear
   ```
2. Restart MySQL server
3. Run database optimization:
   ```bash
   mysql -u root -p logistic < optimize.sql
   ```

## 📁 Project Structure After Setup

```
projects/datasets/
├── app.py                      # Main Streamlit app
├── database.py                 # Database management
├── data_ingestion.py          # Data loading
├── queries.py                 # SQL queries
├── setup.py                   # Setup wizard
├── requirements.txt           # Dependencies
├── run.bat                    # Windows launcher
├── run.sh                     # Linux/Mac launcher
├── README.md                  # Documentation
├── SETUP_GUIDE.md             # This file
├── .gitignore                 # Git ignore file
├── .streamlit/                # Streamlit config
│   └── config.toml
├── venv/                      # Virtual environment (created)
├── shipments.json             # Data file
├── shipment_tracking.csv      # Data file
├── courier_staff.csv          # Data file
├── routes.csv                 # Data file
├── warehouses.json            # Data file
└── costs.csv                  # Data file
```

## 🧪 Testing & Validation

### Test Database Connection

```bash
python -c "from database import get_connection; conn = get_connection(); print('✅ Connected'); conn.close()"
```

### Test Data Loading

```bash
python data_ingestion.py
```

### Test Queries

```bash
python -c "from queries import LogisticsQueries; print('Total Shipments:', LogisticsQueries.get_total_shipments())"
```

### Run Full System Test

```bash
python setup.py --test
```

## 📈 Initial Data Loading Performance

Expected times (varies by system):

| Dataset | Records | Time |
|---------|---------|------|
| Courier Staff | 1,000 | <5 sec |
| Routes | 500 | <5 sec |
| Warehouses | 300 | <5 sec |
| Shipments | 70,000 | ~30 sec |
| Costs | 70,000 | ~30 sec |
| Tracking | 209,000 | ~60 sec |
| **Total** | **~350,000** | **~3-4 min** |

## 🔐 Security Best Practices

### For Development

- Store credentials in `.env` file (not in code)
- Add `.env` to `.gitignore`
- Never commit sensitive data

### For Production

1. **Use environment variables:**
   ```bash
   export DB_PASSWORD=your_secure_password
   ```

2. **Create limited MySQL user:**
   ```sql
   CREATE USER 'logistics_app'@'localhost' IDENTIFIED BY 'strong_password';
   GRANT SELECT, INSERT, UPDATE ON logistic.* TO 'logistics_app'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Enable SSL for database:**
   - Require SSL connections
   - Use certificate authentication

4. **Implement Streamlit authentication:**
   - Add login/password protection
   - Use OAuth for enterprise

## 💻 Development Tips

### Activate on Startup

**Windows:** Add to `.streamlit/config.toml`
```
[server]
runOnSave = true
```

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Profile Performance

Add timing decorators:
```python
import time

def profile_query(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Query took {time.time() - start:.2f}s")
        return result
    return wrapper
```

## 📚 Additional Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **MySQL Docs:** https://dev.mysql.com/doc
- **Pandas Guide:** https://pandas.pydata.org/docs
- **Plotly Charts:** https://plotly.com/python

## 🎓 Learning Path

1. Understand database schema (README.md)
2. Explore data files (CSV/JSON format)
3. Review SQL queries (queries.py)
4. Study Streamlit components (app.py)
5. Customize visualizations
6. Deploy to production

## 🆘 Getting Help

### Check Logs

```bash
# Streamlit logs
streamlit logs

# Python console
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
```

### Common Commands

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Deactivate
deactivate

# Install package
pip install package_name

# List installed packages
pip list

# Update all packages
pip install --upgrade -r requirements.txt

# Clear Streamlit cache
streamlit cache clear

# Run specific app with port
streamlit run app.py --server.port 8502
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] MySQL server is running
- [ ] Database `logistic` exists
- [ ] All CSV/JSON files are present
- [ ] Python dependencies installed
- [ ] `python database.py` initializes successfully
- [ ] `python data_ingestion.py` loads data without errors
- [ ] `streamlit run app.py` starts successfully
- [ ] Dashboard opens in browser
- [ ] KPI metrics display correctly
- [ ] Search and filter functions work
- [ ] Charts render without errors
- [ ] No database connection errors in console

---

**Congratulations!** 🎉 Your Smart Logistics Dashboard is now ready to use!

For more information, see [README.md](README.md)

**Last Updated:** February 2026  
**Version:** 1.0
