import polars as pl


def transform_stockmarket(data: pl.DataFrame) -> pl.DataFrame:
    """ Transform data

    Args:
        data (pl.DataFrame): Raw data

    Notes:
        Create rolling window columns (moving average, rolling median)

    Returns:
        pl.DataFrame: Transformed data
    """

    # Remove null values if any of the columns are null
    data = data.drop_nulls(subset=["Date", "Adj Close", "Volume", "Symbol"])

    # Convert string to date (used for sorting and creating the moving average)
    data = data.with_columns(
        pl.col("Date").str.to_datetime("%Y-%m-%d").cast(pl.Datetime)
    )

    # Add rolling window columns
    data_agg = (
        data.sort("Symbol", "Date")
        .groupby_rolling(index_column="Date", by="Symbol", period="30d")
        .agg(
            [
                pl.last("Volume").alias("Volume"),
                pl.mean("Volume").alias("vol_moving_avg"),
                pl.median("Adj Close").alias("adj_close_rolling_med"),
            ]
        )
    )

    return data_agg
