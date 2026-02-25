"""
SQL queries module for logistics analytics and KPI calculations.
Contains optimized queries for insights and performance metrics.
"""

from database import get_connection
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LogisticsQueries:
    """Container for all logistics-related SQL queries."""
    
    @staticmethod
    def get_connection_and_execute(query, params=None):
        """
        Execute a query and return results as pandas DataFrame.
        
        Args:
            query (str): SQL query
            params (tuple): Query parameters
            
        Returns:
            pandas.DataFrame: Query results
        """
        try:
            conn = get_connection()
            if params:
                df = pd.read_sql(query, conn, params=params)
            else:
                df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    # ========== OPERATIONAL KPIs ==========
    
    @staticmethod
    def get_total_shipments():
        """Get total number of shipments."""
        query = "SELECT COUNT(*) as total_shipments FROM shipments"
        result = LogisticsQueries.get_connection_and_execute(query)
        return result.iloc[0, 0]
    
    @staticmethod
    def get_delivered_percentage():
        """Get percentage of delivered shipments."""
        query = """
            SELECT 
                ROUND(COUNT(CASE WHEN status = 'Delivered' THEN 1 END) * 100.0 / COUNT(*), 2) 
                as delivered_percentage
            FROM shipments
        """
        result = LogisticsQueries.get_connection_and_execute(query)
        return result.iloc[0, 0]
    
    @staticmethod
    def get_cancelled_percentage():
        """Get percentage of cancelled shipments."""
        query = """
            SELECT 
                ROUND(COUNT(CASE WHEN status = 'Cancelled' THEN 1 END) * 100.0 / COUNT(*), 2) 
                as cancelled_percentage
            FROM shipments
        """
        result = LogisticsQueries.get_connection_and_execute(query)
        return result.iloc[0, 0]
    
    @staticmethod
    def get_intransit_percentage():
        """Get percentage of in-transit shipments."""
        query = """
            SELECT 
                ROUND(COUNT(CASE WHEN status = 'In Transit' THEN 1 END) * 100.0 / COUNT(*), 2) 
                as intransit_percentage
            FROM shipments
        """
        result = LogisticsQueries.get_connection_and_execute(query)
        return result.iloc[0, 0]
    
    @staticmethod
    def get_average_delivery_time():
        """Get average delivery time in days."""
        query = """
            SELECT 
                ROUND(AVG(DATEDIFF(delivery_date, order_date)), 2) as avg_delivery_days
            FROM shipments
            WHERE status = 'Delivered' AND delivery_date IS NOT NULL
        """
        result = LogisticsQueries.get_connection_and_execute(query)
        return result.iloc[0, 0]
    
    @staticmethod
    def get_total_operational_cost():
        """Get total operational cost across all shipments."""
        query = """
            SELECT 
                ROUND(SUM(fuel_cost + labor_cost + misc_cost), 2) as total_cost
            FROM costs
        """
        result = LogisticsQueries.get_connection_and_execute(query)
        return result.iloc[0, 0]
    
    # ========== DELIVERY PERFORMANCE ==========
    
    @staticmethod
    def get_average_delivery_time_per_route():
        """Get average delivery time by route."""
        query = """
            SELECT 
                s.origin,
                s.destination,
                ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 2) as avg_days,
                COUNT(s.shipment_id) as num_shipments,
                r.distance_km,
                r.avg_time_hours
            FROM shipments s
            LEFT JOIN routes r ON s.origin = r.origin AND s.destination = r.destination
            WHERE s.status = 'Delivered' AND s.delivery_date IS NOT NULL
            GROUP BY s.origin, s.destination, r.distance_km, r.avg_time_hours
            ORDER BY avg_days DESC
            LIMIT 20
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_most_delayed_routes():
        """Get top delayed routes with shipment counts."""
        query = """
            SELECT 
                s.origin,
                s.destination,
                ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 2) as avg_delivery_days,
                COUNT(s.shipment_id) as num_shipments,
                r.avg_time_hours,
                ROUND(r.distance_km, 2) as distance_km
            FROM shipments s
            LEFT JOIN routes r ON s.origin = r.origin AND s.destination = r.destination
            WHERE s.status = 'Delivered' AND s.delivery_date IS NOT NULL
            GROUP BY s.origin, s.destination, r.avg_time_hours, r.distance_km
            ORDER BY avg_delivery_days DESC
            LIMIT 15
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_delivery_time_vs_distance():
        """Compare delivery time ratio against distance."""
        query = """
            SELECT 
                s.origin,
                s.destination,
                ROUND(r.distance_km, 2) as distance_km,
                ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 2) as avg_delivery_days,
                ROUND(r.avg_time_hours / 24, 2) as expected_days,
                ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)) - (r.avg_time_hours / 24), 2) as delay_days,
                COUNT(s.shipment_id) as num_shipments
            FROM shipments s
            LEFT JOIN routes r ON s.origin = r.origin AND s.destination = r.destination
            WHERE s.status = 'Delivered' AND s.delivery_date IS NOT NULL
            GROUP BY s.origin, s.destination, r.distance_km, r.avg_time_hours
            ORDER BY delay_days DESC
            LIMIT 20
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    # ========== COURIER PERFORMANCE ==========
    
    @staticmethod
    def get_courier_performance():
        """Get shipment statistics per courier."""
        query = """
            SELECT 
                c.courier_id,
                c.name,
                c.vehicle_type,
                c.rating,
                COUNT(s.shipment_id) as num_shipments,
                COUNT(CASE WHEN s.status = 'Delivered' THEN 1 END) as delivered_count,
                COUNT(CASE WHEN s.status = 'Cancelled' THEN 1 END) as cancelled_count,
                ROUND(COUNT(CASE WHEN s.status = 'Delivered' THEN 1 END) * 100.0 / COUNT(s.shipment_id), 2) as delivery_rate
            FROM courier_staff c
            LEFT JOIN shipments s ON c.courier_id = s.courier_id
            GROUP BY c.courier_id, c.name, c.vehicle_type, c.rating
            ORDER BY num_shipments DESC
            LIMIT 30
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_ontime_delivery_by_courier():
        """Get on-time delivery performance by courier."""
        query = """
            SELECT 
                c.courier_id,
                c.name,
                c.rating,
                COUNT(s.shipment_id) as total_shipments,
                COUNT(CASE WHEN s.status = 'Delivered' THEN 1 END) as delivered,
                ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 2) as avg_days,
                ROUND(COUNT(CASE WHEN s.status = 'Delivered' THEN 1 END) * 100.0 / COUNT(s.shipment_id), 2) as delivery_success_rate
            FROM courier_staff c
            LEFT JOIN shipments s ON c.courier_id = s.courier_id
            WHERE s.status = 'Delivered' AND s.delivery_date IS NOT NULL
            GROUP BY c.courier_id, c.name, c.rating
            HAVING delivered > 0
            ORDER BY delivery_success_rate DESC, avg_days ASC
            LIMIT 20
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_courier_rating_comparison():
        """Compare courier performance by rating."""
        query = """
            SELECT 
                c.rating,
                COUNT(s.shipment_id) as num_shipments,
                COUNT(CASE WHEN s.status = 'Delivered' THEN 1 END) as delivered,
                ROUND(COUNT(CASE WHEN s.status = 'Delivered' THEN 1 END) * 100.0 / COUNT(s.shipment_id), 2) as delivery_rate,
                ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 2) as avg_delivery_days
            FROM courier_staff c
            LEFT JOIN shipments s ON c.courier_id = s.courier_id
            WHERE s.status = 'Delivered' AND s.delivery_date IS NOT NULL
            GROUP BY c.rating
            ORDER BY c.rating DESC
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    # ========== COST ANALYTICS ==========
    
    @staticmethod
    def get_cost_per_shipment():
        """Get individual shipment costs with details."""
        query = """
            SELECT 
                c.shipment_id,
                s.origin,
                s.destination,
                s.weight,
                ROUND(c.fuel_cost, 2) as fuel_cost,
                ROUND(c.labor_cost, 2) as labor_cost,
                ROUND(c.misc_cost, 2) as misc_cost,
                ROUND(c.fuel_cost + c.labor_cost + c.misc_cost, 2) as total_cost,
                s.status
            FROM costs c
            JOIN shipments s ON c.shipment_id = s.shipment_id
            ORDER BY (c.fuel_cost + c.labor_cost + c.misc_cost) DESC
            LIMIT 50
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_cost_per_route():
        """Get aggregate costs by route."""
        query = """
            SELECT 
                s.origin,
                s.destination,
                ROUND(SUM(c.fuel_cost), 2) as total_fuel_cost,
                ROUND(SUM(c.labor_cost), 2) as total_labor_cost,
                ROUND(SUM(c.misc_cost), 2) as total_misc_cost,
                ROUND(SUM(c.fuel_cost + c.labor_cost + c.misc_cost), 2) as total_cost,
                COUNT(c.shipment_id) as num_shipments,
                ROUND(AVG(c.fuel_cost + c.labor_cost + c.misc_cost), 2) as avg_cost_per_shipment
            FROM costs c
            JOIN shipments s ON c.shipment_id = s.shipment_id
            GROUP BY s.origin, s.destination
            ORDER BY total_cost DESC
            LIMIT 25
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_fuel_vs_labor_contribution():
        """Get fuel vs labor cost contribution percentages."""
        query = """
            SELECT 
                ROUND(SUM(fuel_cost) * 100.0 / (SUM(fuel_cost) + SUM(labor_cost) + SUM(misc_cost)), 2) as fuel_percent,
                ROUND(SUM(labor_cost) * 100.0 / (SUM(fuel_cost) + SUM(labor_cost) + SUM(misc_cost)), 2) as labor_percent,
                ROUND(SUM(misc_cost) * 100.0 / (SUM(fuel_cost) + SUM(labor_cost) + SUM(misc_cost)), 2) as misc_percent
            FROM costs
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_high_cost_shipments():
        """Get shipments with highest costs."""
        query = """
            SELECT 
                c.shipment_id,
                s.origin,
                s.destination,
                s.weight,
                ROUND(c.fuel_cost + c.labor_cost + c.misc_cost, 2) as total_cost,
                ROUND((c.fuel_cost + c.labor_cost + c.misc_cost) / NULLIF(s.weight, 0), 2) as cost_per_kg,
                s.status
            FROM costs c
            JOIN shipments s ON c.shipment_id = s.shipment_id
            ORDER BY (c.fuel_cost + c.labor_cost + c.misc_cost) DESC
            LIMIT 30
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    # ========== CANCELLATION ANALYSIS ==========
    
    @staticmethod
    def get_cancellation_rate_by_origin():
        """Get cancellation rate by origin city."""
        query = """
            SELECT 
                origin,
                COUNT(shipment_id) as total_shipments,
                COUNT(CASE WHEN status = 'Cancelled' THEN 1 END) as cancelled,
                ROUND(COUNT(CASE WHEN status = 'Cancelled' THEN 1 END) * 100.0 / COUNT(shipment_id), 2) as cancellation_rate
            FROM shipments
            GROUP BY origin
            ORDER BY cancellation_rate DESC
            LIMIT 25
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_cancellation_rate_by_courier():
        """Get cancellation rate by courier."""
        query = """
            SELECT 
                c.courier_id,
                c.name,
                COUNT(s.shipment_id) as total_shipments,
                COUNT(CASE WHEN s.status = 'Cancelled' THEN 1 END) as cancelled,
                ROUND(COUNT(CASE WHEN s.status = 'Cancelled' THEN 1 END) * 100.0 / COUNT(s.shipment_id), 2) as cancellation_rate
            FROM courier_staff c
            LEFT JOIN shipments s ON c.courier_id = s.courier_id
            GROUP BY c.courier_id, c.name
            HAVING total_shipments > 0
            ORDER BY cancellation_rate DESC
            LIMIT 20
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_time_to_cancellation():
        """Get average time from order to cancellation."""
        query = """
            SELECT 
                s.origin,
                s.destination,
                COUNT(s.shipment_id) as cancelled_count,
                ROUND(AVG(DATEDIFF(DATE(st.timestamp), s.order_date)), 2) as avg_days_to_cancel
            FROM shipments s
            JOIN shipment_tracking st ON s.shipment_id = st.shipment_id
            WHERE s.status = 'Cancelled' AND st.status = 'Cancelled'
            GROUP BY s.origin, s.destination
            ORDER BY avg_days_to_cancel ASC
            LIMIT 20
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    # ========== WAREHOUSE INSIGHTS ==========
    
    @staticmethod
    def get_warehouse_capacity_comparison():
        """Get warehouse capacity and utilization."""
        query = """
            SELECT 
                w.warehouse_id,
                w.city,
                w.state,
                w.capacity,
                COUNT(s.shipment_id) as num_shipments,
                ROUND(COUNT(s.shipment_id) * 100.0 / w.capacity, 2) as utilization_rate
            FROM warehouses w
            LEFT JOIN shipments s ON w.city = s.origin
            GROUP BY w.warehouse_id, w.city, w.state, w.capacity
            ORDER BY utilization_rate DESC
            LIMIT 25
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_high_traffic_warehouses():
        """Get warehouses with highest traffic."""
        query = """
            SELECT 
                w.city,
                w.state,
                COUNT(DISTINCT s.shipment_id) as num_shipments,
                COUNT(DISTINCT s.courier_id) as num_couriers,
                ROUND(AVG(s.weight), 2) as avg_weight,
                w.capacity
            FROM warehouses w
            LEFT JOIN shipments s ON w.city = s.origin
            GROUP BY w.city, w.state, w.capacity
            ORDER BY num_shipments DESC
            LIMIT 20
        """
        return LogisticsQueries.get_connection_and_execute(query)
    
    # ========== SEARCH & FILTER ==========
    
    @staticmethod
    def search_shipment(shipment_id):
        """Search for a shipment by ID."""
        query = """
            SELECT 
                s.*,
                c.fuel_cost + c.labor_cost + c.misc_cost as total_cost
            FROM shipments s
            LEFT JOIN costs c ON s.shipment_id = c.shipment_id
            WHERE s.shipment_id = %s
        """
        return LogisticsQueries.get_connection_and_execute(query, (shipment_id,))
    
    @staticmethod
    def filter_shipments(status=None, origin=None, destination=None, start_date=None, end_date=None, courier_id=None):
        """Filter shipments based on multiple criteria."""
        query = "SELECT * FROM shipments WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = %s"
            params.append(status)
        if origin:
            query += " AND origin = %s"
            params.append(origin)
        if destination:
            query += " AND destination = %s"
            params.append(destination)
        if start_date:
            query += " AND order_date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND order_date <= %s"
            params.append(end_date)
        if courier_id:
            query += " AND courier_id = %s"
            params.append(courier_id)
        
        query += " LIMIT 1000"
        
        return LogisticsQueries.get_connection_and_execute(query, tuple(params) if params else None)
    
    @staticmethod
    def get_shipment_tracking_history(shipment_id):
        """Get complete tracking history for a shipment."""
        query = """
            SELECT 
                tracking_id,
                status,
                timestamp
            FROM shipment_tracking
            WHERE shipment_id = %s
            ORDER BY timestamp ASC
        """
        return LogisticsQueries.get_connection_and_execute(query, (shipment_id,))
    
    @staticmethod
    def get_unique_origins():
        """Get list of unique origin cities."""
        query = "SELECT DISTINCT origin FROM shipments ORDER BY origin"
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_unique_destinations():
        """Get list of unique destination cities."""
        query = "SELECT DISTINCT destination FROM shipments ORDER BY destination"
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_unique_couriers():
        """Get list of unique couriers."""
        query = "SELECT courier_id, name FROM courier_staff ORDER BY name"
        return LogisticsQueries.get_connection_and_execute(query)
    
    @staticmethod
    def get_shipment_statuses():
        """Get list of unique shipment statuses."""
        query = "SELECT DISTINCT status FROM shipments ORDER BY status"
        return LogisticsQueries.get_connection_and_execute(query)


if __name__ == "__main__":
    # Test queries
    print("Total Shipments:", LogisticsQueries.get_total_shipments())
    print("Delivered %:", LogisticsQueries.get_delivered_percentage())
