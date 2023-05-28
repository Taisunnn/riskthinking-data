from typing import Tuple

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


def stockmarket_train_model(data: pd.DataFrame) -> Tuple[RandomForestRegressor, float, float]:
    """ Train a Model on the data

    Args:
        data (pd.DataFrame): Data to train the model on

    Returns:
        [RandomForestRegressor, float, float]: Trained model, Mean Absolute Error, Mean Squared Error

    """
    # Assume `data` is loaded as a Pandas DataFrame
    data["Date"] = pd.to_datetime(data["Date"])
    data.set_index("Date", inplace=True)

    # Select features and target
    features = ["vol_moving_avg", "adj_close_rolling_med"]
    target = "Volume"

    X = data[features]
    y = data[target]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Create a RandomForestRegressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on test data
    y_pred = model.predict(X_test)

    # Calculate the Mean Absolute Error and Mean Squared Error
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    return model, mae, mse
