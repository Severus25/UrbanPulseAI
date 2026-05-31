"""Airflow DAG: Weather Data Ingestion

Runs hourly to fetch weather forecasts and alerts.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "urbanpulse",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

dag = DAG(
    "weather_ingestion",
    default_args=default_args,
    description="Ingest weather forecasts and alerts",
    schedule_interval="0 * * * *",  # Hourly
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["weather", "ingestion"],
)


def fetch_weather_forecast(**context):
    """Fetch weather forecast from OpenWeatherMap API."""
    # TODO: Call OpenWeatherMap One Call API
    pass


def fetch_weather_alerts(**context):
    """Fetch active weather alerts."""
    pass


def compute_weather_risk(**context):
    """Compute flooding/heat risk scores based on forecast."""
    # TODO: Apply thresholds to precipitation, temperature
    pass


fetch_forecast = PythonOperator(
    task_id="fetch_weather_forecast", python_callable=fetch_weather_forecast, dag=dag
)
fetch_alerts = PythonOperator(
    task_id="fetch_weather_alerts", python_callable=fetch_weather_alerts, dag=dag
)
compute_risk = PythonOperator(
    task_id="compute_weather_risk", python_callable=compute_weather_risk, dag=dag
)

[fetch_forecast, fetch_alerts] >> compute_risk
