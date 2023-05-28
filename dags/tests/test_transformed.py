import polars as pl
import pandera as pa

from stockmarket.common.transforms import transform_stockmarket


def test_transformed():
    """ Test column integrity after data gets transformed """

    data = pl.read_csv("data_in/test/stockmarket_test.csv")

    # Transform data
    data = transform_stockmarket(data)

    # Defining schema checks on date
    schema = pa.DataFrameSchema(
        columns={
            "Symbol": pa.Column(pa.String),
            "Date": pa.Column(pa.DateTime),
            "Volume": pa.Column(pa.Float),
            "vol_moving_avg": pa.Column(pa.Float),
            "adj_close_rolling_med": pa.Column(pa.Float),
        }
    )

    # Validate dataframe (need to turn into pandas dataframe; supported by pandera)
    schema.validate(data.to_pandas())
