# Stockmarket Ingestion and Machine Learning (RiskThinkingAI)

This is a pipeline that downloads stock market data from Kaggle, transforms the data, and trains a model on the transformed data.
___
# Getting Started

## Prerequisites
* Docker Engine

## Cloning Repository
```
git clone https://github.com/Taisunnn/riskthinking-data.git

cd riskthinking-data
```
## Local Environment (Commands)
```
make start (starts the docker containers)

make stop (stops the docker containers)

make test (runs pytest within the container)

make lint (runs flake8 within the container)
```
## Accessing Web Servers

### Airflow UI

#### https://0.0.0.0:8080 (Airflow username and password can be found in the terminal)

### FastAPI App

#### https://0.0.0.0:8000
___

# Workflow (DAG)
1. Raw Data Ingestion
2. Transform Data
3. Train Model

# Problem 1 & 2
## Raw Data Processing & Feature Engineering:
* Instead of using Pandas, **Polars** would be more suitable because it is much **faster** and more **memory efficient** than Pandas; (transformations, joins, group by). If we need something that can process larger datasets, we should use Spark because any data that it cannot fit in memory can spill to disk.
* Running "make test" will run pytest within the container and will check for dataframe column integrity with Pandera after the data has been transformed.

# Problem 3
## Model Implementation:
* There are many ways we can implement a machine learning model. The random forest regressor works well out of the box without much tuning. Given that this problem is time series based, I would have constructed the split by dividing the earlier data for the training set and recent data for the validation set. 
* In order to build a better model it is necessary to choose the most correct hyper parameters for the model. 
    * Libraries such as hyperopt-sklean or optuna can assist with tuning the model to maximize efficiency.

# Problem 4
## API Deployment:
The app is built using the FastAPI framework and deployed on a Hugging Face Space.
Link to the Swagger UI is found below:

**https://taisunnn-riskthinkingai-data-eng.hf.space/docs**

# Acknowledgments / References

1. [Stockmarket Dataset (Kaggle)](https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset)
2. [Python (tempfile)](https://docs.python.org/3/library/tempfile.html)
3. [Polars](https://pola-rs.github.io/polars/py-polars/html/reference/)
4. [Python (Logging Handler)](https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout)
5. [Docker](https://docs.docker.com/engine/reference/builder/)
6. [Pandera](https://pandera.readthedocs.io/en/stable/)
7. [Docker Flake8 Image](https://hub.docker.com/r/alpine/flake8)


