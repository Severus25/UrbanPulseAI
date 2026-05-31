"""Airflow DAG: Traffic Data Ingestion Pipeline

Runs every 5 minutes to ingest live traffic data from configured sources,
process it, and store in PostGIS + publish to Kafka.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "urbanpulse",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "traffic_ingestion",
    default_args=default_args,
    description="Ingest real-time traffic speed data",
    schedule_interval="*/5 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["traffic", "ingestion"],
)


def fetch_traffic_data(**context):
    """Fetch traffic speed data from external APIs."""
    # TODO: Implement API calls to traffic data providers
    # Examples: TomTom, HERE, NYC Open Data, etc.
    pass


def process_traffic_data(**context):
    """Map-match and aggregate to road segments."""
    # TODO: Map match GPS points to road network
    # TODO: Aggregate speeds per segment
    pass


def store_traffic_data(**context):
    """Store processed data in PostGIS and publish to Kafka."""
    # TODO: Insert into PostGIS
    # TODO: Publish to Kafka topic 'traffic.speed.realtime'
    pass


def update_features(**context):
    """Update feature store with latest traffic features."""
    # TODO: Compute lag features, rolling averages
    pass


fetch = PythonOperator(task_id="fetch_traffic_data", python_callable=fetch_traffic_data, dag=dag)
process = PythonOperator(task_id="process_traffic_data", python_callable=process_traffic_data, dag=dag)
store = PythonOperator(task_id="store_traffic_data", python_callable=store_traffic_data, dag=dag)
features = PythonOperator(task_id="update_features", python_callable=update_features, dag=dag)

fetch >> process >> store >> features
