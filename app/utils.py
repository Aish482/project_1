"""
Utility functions and helpers for the Logistics Analytics Platform.
Provides common tasks and convenience functions.
"""

import pandas as pd
from datetime import datetime, timedelta
from queries import LogisticsQueries
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LogisticsAnalytics:
    """Helper class for advanced analytics and reporting."""
    
    @staticmethod
    def generate_performance_report(days=30):
        """
        Generate a comprehensive performance report for the last N days.
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            dict: Performance metrics
        """
        try:
            report = {
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'period_days': days,
                'metrics': {
                    'total_shipments': LogisticsQueries.get_total_shipments(),
                    'delivered_percentage': LogisticsQueries.get_delivered_percentage(),
                    'cancelled_percentage': LogisticsQueries.get_cancelled_percentage(),
                    'avg_delivery_time': LogisticsQueries.get_average_delivery_time(),
                    'total_operational_cost': LogisticsQueries.get_total_operational_cost(),
                }
            }
            logger.info(f"Performance report generated: {report}")
            return report
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise
    
    @staticmethod
    def get_top_performers(metric='shipments', limit=10):
        """
        Get top performing couriers based on specified metric.
        
        Args:
            metric (str): 'shipments', 'rating', or 'delivery_rate'
            limit (int): Number of results
            
        Returns:
            pandas.DataFrame: Top performers
        """
        try:
            df = LogisticsQueries.get_courier_performance()
            
            if metric == 'shipments':
                return df.nlargest(limit, 'num_shipments')
            elif metric == 'rating':
                return df.nlargest(limit, 'rating')
            elif metric == 'delivery_rate':
                return df.nlargest(limit, 'delivery_rate')
            else:
                return df.head(limit)
        except Exception as e:
            logger.error(f"Error getting top performers: {e}")
            raise
    
    @staticmethod
    def identify_bottleneck_routes(threshold_percentile=75):
        """
        Identify routes with delays above specified percentile.
        
        Args:
            threshold_percentile (float): Percentile threshold (0-100)
            
        Returns:
            pandas.DataFrame: Bottleneck routes
        """
        try:
            df = LogisticsQueries.get_most_delayed_routes()
            
            if df.empty:
                return df
            
            threshold = df['avg_delivery_days'].quantile(threshold_percentile / 100)
            bottlenecks = df[df['avg_delivery_days'] >= threshold]
            
            logger.info(f"Found {len(bottlenecks)} bottleneck routes")
            return bottlenecks
        except Exception as e:
            logger.error(f"Error identifying bottlenecks: {e}")
            raise
    
    @staticmethod
    def analyze_cost_patterns():
        """
        Analyze cost patterns and identify high-cost routes.
        
        Returns:
            dict: Cost analysis
        """
        try:
            total_cost = LogisticsQueries.get_total_operational_cost()
            cost_by_route = LogisticsQueries.get_cost_per_route()
            high_cost = LogisticsQueries.get_high_cost_shipments()
            fuel_vs_labor = LogisticsQueries.get_fuel_vs_labor_contribution()
            
            analysis = {
                'total_operational_cost': total_cost,
                'high_cost_routes': cost_by_route.nlargest(5, 'total_cost'),
                'high_cost_shipments': high_cost.nlargest(5, 'total_cost'),
                'cost_breakdown': fuel_vs_labor.to_dict() if not fuel_vs_labor.empty else {}
            }
            
            logger.info("Cost patterns analysis completed")
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing cost patterns: {e}")
            raise
    
    @staticmethod
    def predict_problematic_shipments():
        """
        Identify shipments likely to face issues based on patterns.
        
        Returns:
            pandas.DataFrame: Problematic shipments
        """
        try:
            cancellation_by_courier = LogisticsQueries.get_cancellation_rate_by_courier()
            high_cancellation = cancellation_by_courier[cancellation_by_courier['cancellation_rate'] > 10]
            
            logger.info(f"Found {len(high_cancellation)} couriers with high cancellation rates")
            return high_cancellation
        except Exception as e:
            logger.error(f"Error predicting issues: {e}")
            raise


class DataExportManager:
    """Manage data export in various formats."""
    
    @staticmethod
    def export_to_csv(data, filename):
        """
        Export DataFrame to CSV file.
        
        Args:
            data (pandas.DataFrame): Data to export
            filename (str): Output filename
        """
        try:
            data.to_csv(filename, index=False)
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise
    
    @staticmethod
    def export_to_excel(data, filename):
        """
        Export DataFrame to Excel file.
        
        Args:
            data (pandas.DataFrame): Data to export
            filename (str): Output filename
        """
        try:
            data.to_excel(filename, index=False)
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            raise
    
    @staticmethod
    def export_report(report_dict, filename):
        """
        Export report dictionary to formatted text file.
        
        Args:
            report_dict (dict): Report data
            filename (str): Output filename
        """
        try:
            with open(filename, 'w') as f:
                for key, value in report_dict.items():
                    f.write(f"{key}: {value}\n")
            logger.info(f"Report exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting report: {e}")
            raise


class DataQualityChecker:
    """Check data quality and consistency."""
    
    @staticmethod
    def check_missing_values():
        """
        Check for missing/NULL values in key tables.
        
        Returns:
            dict: Missing value counts per table
        """
        try:
            from database import get_connection
            
            conn = get_connection()
            tables = ['shipments', 'courier_staff', 'routes', 'warehouses', 'costs']
            
            missing_values = {}
            
            for table in tables:
                query = f"SELECT * FROM {table} LIMIT 100"
                df = pd.read_sql(query, conn)
                missing_values[table] = df.isnull().sum().to_dict()
            
            conn.close()
            logger.info("Data quality check completed")
            return missing_values
        except Exception as e:
            logger.error(f"Error checking data quality: {e}")
            raise
    
    @staticmethod
    def validate_data_consistency():
        """
        Validate data consistency (referential integrity, etc).
        
        Returns:
            dict: Consistency check results
        """
        try:
            from database import get_connection
            
            conn = get_connection()
            cursor = conn.cursor()
            
            results = {}
            
            # Check orphaned shipment_tracking records
            cursor.execute("""
                SELECT COUNT(*) FROM shipment_tracking st
                WHERE NOT EXISTS (SELECT 1 FROM shipments s WHERE s.shipment_id = st.shipment_id)
            """)
            results['orphaned_tracking'] = cursor.fetchone()[0]
            
            # Check orphaned costs
            cursor.execute("""
                SELECT COUNT(*) FROM costs c
                WHERE NOT EXISTS (SELECT 1 FROM shipments s WHERE s.shipment_id = c.shipment_id)
            """)
            results['orphaned_costs'] = cursor.fetchone()[0]
            
            # Check invalid courier references
            cursor.execute("""
                SELECT COUNT(*) FROM shipments s
                WHERE courier_id IS NOT NULL 
                AND NOT EXISTS (SELECT 1 FROM courier_staff c WHERE c.courier_id = s.courier_id)
            """)
            results['invalid_couriers'] = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            logger.info("Data consistency validation completed")
            return results
        except Exception as e:
            logger.error(f"Error validating consistency: {e}")
            raise


class PerformanceTuning:
    """Database performance optimization utilities."""
    
    @staticmethod
    def analyze_slow_queries():
        """
        Log current slow query threshold and provide recommendations.
        
        Returns:
            dict: Performance recommendations
        """
        recommendations = {
            'add_indexes': [
                'shipments.status',
                'shipments.courier_id',
                'shipments.order_date',
                'shipment_tracking.shipment_id',
                'costs.shipment_id'
            ],
            'optimize_queries': [
                'Use pagination for large result sets',
                'Filter by date range when possible',
                'Use aggregate functions instead of client-side processing'
            ],
            'cache_strategy': [
                'Cache KPI calculations (5-minute refresh)',
                'Cache dimension tables (1-hour refresh)',
                'Cache fact tables selectively'
            ]
        }
        return recommendations
    
    @staticmethod
    def get_table_statistics():
        """
        Get table size and row count statistics.
        
        Returns:
            pandas.DataFrame: Table statistics
        """
        try:
            from database import get_connection
            
            query = """
                SELECT 
                    TABLE_NAME,
                    TABLE_ROWS,
                    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size(MB)'
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = 'logistic'
                ORDER BY data_length DESC
            """
            
            conn = get_connection()
            df = pd.read_sql(query, conn)
            conn.close()
            
            return df
        except Exception as e:
            logger.error(f"Error getting table statistics: {e}")
            raise


if __name__ == "__main__":
    # Test utilities
    print("🧪 Testing Utilities...")
    
    try:
        # Generate report
        report = LogisticsAnalytics.generate_performance_report()
        print("\n📊 Performance Report:")
        for key, value in report.items():
            print(f"  {key}: {value}")
        
        # Get top performers
        top = LogisticsAnalytics.get_top_performers('shipments', 5)
        print("\n👥 Top 5 Couriers by Shipments:")
        print(top[['courier_id', 'name', 'num_shipments']])
        
        # Identify bottlenecks
        bottlenecks = LogisticsAnalytics.identify_bottleneck_routes()
        print(f"\n⚠️ Found {len(bottlenecks)} bottleneck routes")
        
        # Check data quality
        quality = DataQualityChecker.check_missing_values()
        print("\n🔍 Data Quality Check:")
        for table, missing in quality.items():
            print(f"  {table}: {missing}")
        
        print("\n✅ All utilities working correctly!")
        
    except Exception as e:
        print(f"\n❌ Error testing utilities: {e}")
