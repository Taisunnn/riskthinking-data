"""
# Stock Market Pipeline

This is a simple pipeline that downloads stock market data from Kaggle, transforms the data, and trains a model on the transformed data.

## Pipeline Steps

1. Download data from Kaggle
2. Transform data
3. Train model
"""

import logging
import joblib
from datetime import datetime

import pandas as pd
import polars as pl
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from stockmarket.common.datasets import stockmarket
from stockmarket.common.transforms import transform_stockmarket
from stockmarket.common.model import stockmarket_train_model


# Logging File Handler (Airflow also automaticaly logs)
# logPath = ""
# fileName = ""
# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# rootLogger = logging.getLogger()

# fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)


def download_data():
    """ Download data from Kaggle """

    # Download data from Kaggle
    data = stockmarket()

    # NOTE: Writing the data locally, but in a production setting, you would want to store the data somewhere else (ex. Cloud Storage Bucket)
    logging.info("Writing data to csv...")
    data.write_csv("data_in/clean/stocks_etfs.csv", batch_size=50000)

    logging.info("Done writing data to csv!")

    # Write to parquet
    # data.write_parquet("data_in/clean/stocks_etfs.parquet")


def transform_data():
    """ Transform data for Model Training """

    data = pl.read_csv("data_in/clean/stocks_etfs.csv")

    data_ = transform_stockmarket(data)

    # Write to csv
    data_.write_csv("data_in/transformed/stocks_etfs_agg.csv")

    # Write to parquet
    # data_.write_parquet("data_in/transformed/stocks_etfs_agg.parquet")


def train_model():
    """ Train model on transformed data and save to disk """

    # Read transformed data
    data = pd.read_csv("data_in/transformed/stocks_etfs_agg.csv")

    # Train the model
    model, mae, mse = stockmarket_train_model(data)

    # Log model metrics
    logging.info(f"Mean Absolute Error: {mae}")
    logging.info(f"Mean Squared Error: {mse}")

    # Save model to disk
    joblib.dump(model, "model/model.pkl")


default_args = {
    "owner": "Tyson",
    "start_date": datetime(2023, 5, 22),
}

dag = DAG("stockmarket_pipeline", default_args=default_args, schedule_interval=None, doc_md=__doc__)


download_data_operator = PythonOperator(
    task_id="download_data", python_callable=download_data, dag=dag
)

transform_data_operator = PythonOperator(
    task_id="transform_data", python_callable=transform_data, dag=dag
)

train_model_operator = PythonOperator(
    task_id="train_model", python_callable=train_model, dag=dag
)


download_data_operator >> transform_data_operator >> train_model_operator
