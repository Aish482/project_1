"""
Smart Logistics Management & Analytics Platform
Main Streamlit Dashboard Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging

# Import custom modules
from database import get_connection, create_tables
from queries import LogisticsQueries
from data_ingestion import ingest_all_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="Logistics Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header-title {
        color: #1f77d2;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_database():
    """Initialize database and load data if needed."""
    try:
        create_tables()
        st.success("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        st.error(f"Database error: {e}")


def display_kpis():
    """Display operational KPI metrics."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    try:
        total_shipments = LogisticsQueries.get_total_shipments()
        delivered_pct = LogisticsQueries.get_delivered_percentage()
        cancelled_pct = LogisticsQueries.get_cancelled_percentage()
        avg_delivery_time = LogisticsQueries.get_average_delivery_time()
        total_cost = LogisticsQueries.get_total_operational_cost()
        
        with col1:
            st.metric("📦 Total Shipments", f"{total_shipments:,}")
        
        with col2:
            st.metric("✅ Delivered %", f"{delivered_pct or 0:.1f}%")
        
        with col3:
            st.metric("❌ Cancelled %", f"{cancelled_pct or 0:.1f}%")
        
        with col4:
            st.metric("⏱️ Avg Delivery Days", f"{avg_delivery_time or 0:.1f}")
        
        with col5:
            st.metric("💰 Total Cost", f"${total_cost or 0:,.2f}")
    
    except Exception as e:
        st.error(f"Error loading KPIs: {e}")
        logger.error(f"KPI loading error: {e}")


def display_delivery_performance():
    """Display delivery performance insights."""
    st.subheader("📈 Delivery Performance Insights")
    
    try:
        tab1, tab2, tab3 = st.tabs(["Avg Time by Route", "Most Delayed Routes", "Time vs Distance"])
        
        with tab1:
            df = LogisticsQueries.get_average_delivery_time_per_route()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.bar(df.head(15), x='destination', y='avg_days', 
                           title="Average Delivery Days by Destination",
                           labels={'avg_days': 'Days', 'destination': 'Destination'})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            df = LogisticsQueries.get_most_delayed_routes()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.scatter(df, x='distance_km', y='avg_delivery_days', 
                               size='num_shipments', hover_name='destination',
                               title="Delayed Routes (Size = Shipment Count)")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            df = LogisticsQueries.get_delivery_time_vs_distance()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.scatter(df, x='distance_km', y='delay_days',
                               size='num_shipments', hover_name='destination',
                               title="Delivery Delay vs Distance")
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading delivery performance data: {e}")
        logger.error(f"Delivery performance error: {e}")


def display_courier_performance():
    """Display courier performance metrics."""
    st.subheader("👥 Courier Performance")
    
    try:
        tab1, tab2, tab3 = st.tabs(["Overall Performance", "On-Time Delivery", "Rating Comparison"])
        
        with tab1:
            df = LogisticsQueries.get_courier_performance()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.bar(df.head(10), x='name', y='num_shipments',
                           title="Top 10 Couriers by Shipment Count",
                           labels={'num_shipments': 'Shipments', 'name': 'Courier Name'})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            df = LogisticsQueries.get_ontime_delivery_by_courier()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.scatter(df, x='avg_days', y='delivery_success_rate',
                               size='delivered', hover_name='name',
                               title="Courier Delivery Success vs Avg Days")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            df = LogisticsQueries.get_courier_rating_comparison()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.line(df, x='rating', y='delivery_rate',
                            markers=True, title="Delivery Success Rate by Courier Rating")
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading courier performance data: {e}")
        logger.error(f"Courier performance error: {e}")


def display_cost_analytics():
    """Display cost analysis insights."""
    st.subheader("💰 Cost Analytics")
    
    try:
        tab1, tab2, tab3, tab4 = st.tabs(["Top High-Cost", "Cost by Route", "Fuel vs Labor", "Cost per KG"])
        
        with tab1:
            df = LogisticsQueries.get_high_cost_shipments()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.bar(df.head(15), x='shipment_id', y='total_cost',
                           title="Top 15 High-Cost Shipments",
                           labels={'total_cost': 'Cost ($)', 'shipment_id': 'Shipment ID'})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            df = LogisticsQueries.get_cost_per_route()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.bar(df.head(10), x='destination', y='total_cost',
                           title="Top 10 Routes by Total Cost",
                           labels={'total_cost': 'Cost ($)', 'destination': 'Destination'})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            df = LogisticsQueries.get_fuel_vs_labor_contribution()
            if not df.empty:
                fig = go.Figure(data=[go.Pie(
                    labels=['Fuel', 'Labor', 'Misc'],
                    values=[df['fuel_percent'].values[0], 
                           df['labor_percent'].values[0],
                           df['misc_percent'].values[0]],
                    title="Cost Contribution %"
                )])
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(df, use_container_width=True)
        
        with tab4:
            df = LogisticsQueries.get_cost_per_shipment()
            if not df.empty:
                df['cost_per_kg'] = (df['total_cost'] / df['weight']).round(2)
                st.dataframe(df.head(20), use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading cost analytics: {e}")
        logger.error(f"Cost analytics error: {e}")


def display_cancellation_analysis():
    """Display cancellation patterns."""
    st.subheader("❌ Cancellation Analysis")
    
    try:
        tab1, tab2, tab3 = st.tabs(["By Origin", "By Courier", "Time to Cancellation"])
        
        with tab1:
            df = LogisticsQueries.get_cancellation_rate_by_origin()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.bar(df.head(15), x='origin', y='cancellation_rate',
                           title="Cancellation Rate by Origin City",
                           labels={'cancellation_rate': 'Rate (%)', 'origin': 'City'})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            df = LogisticsQueries.get_cancellation_rate_by_courier()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.bar(df.head(10), x='name', y='cancellation_rate',
                           title="Cancellation Rate by Courier",
                           labels={'cancellation_rate': 'Rate (%)', 'name': 'Courier'})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            df = LogisticsQueries.get_time_to_cancellation()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading cancellation analysis: {e}")
        logger.error(f"Cancellation analysis error: {e}")


def display_warehouse_insights():
    """Display warehouse utilization insights."""
    st.subheader("🏢 Warehouse Insights")
    
    try:
        tab1, tab2 = st.tabs(["Capacity Comparison", "High-Traffic Warehouses"])
        
        with tab1:
            df = LogisticsQueries.get_warehouse_capacity_comparison()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                fig = px.bar(df.head(15), x='city', y='utilization_rate',
                           title="Warehouse Utilization Rate (%)",
                           labels={'utilization_rate': 'Rate (%)', 'city': 'City'})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            df = LogisticsQueries.get_high_traffic_warehouses()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading warehouse insights: {e}")
        logger.error(f"Warehouse insights error: {e}")


def display_shipment_search():
    """Display shipment search and filtering interface."""
    st.subheader("🔎 Shipment Search & Filtering")
    
    try:
        # Get filter options
        origins = LogisticsQueries.get_unique_origins()['origin'].tolist()
        destinations = LogisticsQueries.get_unique_destinations()['destination'].tolist()
        couriers_df = LogisticsQueries.get_unique_couriers()
        couriers = [f"{row['courier_id']} - {row['name']}" for _, row in couriers_df.iterrows()]
        statuses = LogisticsQueries.get_shipment_statuses()['status'].tolist()
        
        col1, col2 = st.columns(2)
        
        with col1:
            search_id = st.text_input("Search by Shipment ID", "")
        
        with col2:
            search_button = st.button("🔍 Search", use_container_width=True)
        
        if search_button and search_id:
            result = LogisticsQueries.search_shipment(search_id)
            if not result.empty:
                st.success(f"Found Shipment: {search_id}")
                st.dataframe(result, use_container_width=True)
                
                # Display tracking history
                tracking = LogisticsQueries.get_shipment_tracking_history(search_id)
                if not tracking.empty:
                    st.subheader("📍 Tracking History")
                    st.dataframe(tracking, use_container_width=True)
            else:
                st.warning("Shipment not found")
        
        st.divider()
        st.write("**Apply Filters Below:**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            filter_status = st.selectbox("Status", [None] + statuses, key="filter_status")
        
        with col2:
            filter_origin = st.selectbox("Origin", [None] + origins, key="filter_origin")
        
        with col3:
            filter_destination = st.selectbox("Destination", [None] + destinations, key="filter_destination")
        
        with col4:
            filter_courier = st.selectbox("Courier", [None] + couriers, key="filter_courier")
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=None)
        
        with col2:
            end_date = st.date_input("End Date", value=None)
        
        filter_button = st.button("🔍 Apply Filters", use_container_width=True)
        
        if filter_button:
            courier_id = None
            if filter_courier:
                courier_id = filter_courier.split(" - ")[0]
            
            results = LogisticsQueries.filter_shipments(
                status=filter_status,
                origin=filter_origin,
                destination=filter_destination,
                start_date=start_date,
                end_date=end_date,
                courier_id=courier_id
            )
            
            if not results.empty:
                st.success(f"Found {len(results)} shipments")
                st.dataframe(results, use_container_width=True)
                
                # Display summary statistics
                st.subheader("Summary Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Shipments", len(results))
                
                with col2:
                    delivered = len(results[results['status'] == 'Delivered'])
                    st.metric("Delivered", delivered)
                
                with col3:
                    cancelled = len(results[results['status'] == 'Cancelled'])
                    st.metric("Cancelled", cancelled)
            else:
                st.warning("No shipments found matching the criteria")
    
    except Exception as e:
        st.error(f"Error in shipment search: {e}")
        logger.error(f"Shipment search error: {e}")


def main():
    """Main application function."""
    # Sidebar navigation
    st.sidebar.title("📦 Logistics Analytics")
    st.sidebar.markdown("---")
    
    # Initialize button
    if st.sidebar.button("🔧 Initialize Database"):
        with st.spinner("Initializing database..."):
            initialize_database()
    
    # Data ingestion button
    if st.sidebar.button("📥 Load Data"):
        with st.spinner("Loading data from CSV/JSON files..."):
            try:
                ingest_all_data(".")
                st.sidebar.success("✅ Data loaded successfully!")
            except Exception as e:
                st.sidebar.error(f"Error loading data: {e}")
                logger.error(f"Data loading error: {e}")
    
    st.sidebar.markdown("---")
    
    # Navigation menu
    page = st.sidebar.radio(
        "Navigate to:",
        [
            "🏠 Home",
            "📊 KPI Dashboard",
            "📈 Delivery Performance",
            "👥 Courier Performance",
            "💰 Cost Analytics",
            "❌ Cancellation Analysis",
            "🏢 Warehouse Insights",
            "🔎 Shipment Search"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Smart Logistics Management & Analytics Platform**")
    st.sidebar.markdown("*Powered by Streamlit & MySQL*")
    
    # Page routing
    if page == "🏠 Home":
        st.title("📦 Smart Logistics Management & Analytics Platform")
        st.markdown("---")
        
        st.write("""
        Welcome to the centralized logistics analytics dashboard. This platform provides:
        
        ✅ **Real-time Shipment Tracking** - Monitor delivery status in real-time
        
        📊 **Operational KPI Monitoring** - Track key performance indicators
        
        📈 **Performance Benchmarking** - Compare courier and route efficiency
        
        💰 **Cost Transparency** - Analyze operational costs across shipments
        
        🎯 **Actionable Insights** - Data-driven decisions for logistics optimization
        
        ### Quick Start
        1. **Initialize Database** - Click the button in the sidebar
        2. **Load Data** - Import CSV/JSON files into the database
        3. **Explore Dashboards** - Navigate through different analytical views
        4. **Search & Filter** - Find specific shipments and apply custom filters
        """)
        
        st.subheader("System Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("🗄️ **MySQL Database**\nCentralized data storage with optimized queries")
        
        with col2:
            st.info("📊 **Multi-View Analytics**\nComprehensive insights across all logistics dimensions")
        
        with col3:
            st.info("⚡ **Real-time Dashboard**\nInteractive visualizations and filters")
    
    elif page == "📊 KPI Dashboard":
        st.title("📊 Operational KPI Dashboard")
        st.markdown("---")
        display_kpis()
    
    elif page == "📈 Delivery Performance":
        st.title("📈 Delivery Performance Insights")
        st.markdown("---")
        display_delivery_performance()
    
    elif page == "👥 Courier Performance":
        st.title("👥 Courier Performance Analysis")
        st.markdown("---")
        display_courier_performance()
    
    elif page == "💰 Cost Analytics":
        st.title("💰 Cost Analysis & Optimization")
        st.markdown("---")
        display_cost_analytics()
    
    elif page == "❌ Cancellation Analysis":
        st.title("❌ Shipment Cancellation Analysis")
        st.markdown("---")
        display_cancellation_analysis()
    
    elif page == "🏢 Warehouse Insights":
        st.title("🏢 Warehouse Utilization & Insights")
        st.markdown("---")
        display_warehouse_insights()
    
    elif page == "🔎 Shipment Search":
        st.title("🔎 Shipment Search & Filtering")
        st.markdown("---")
        display_shipment_search()


if __name__ == "__main__":
    main()