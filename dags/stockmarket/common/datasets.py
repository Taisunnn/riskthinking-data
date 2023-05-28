import os
import logging
import glob
import zipfile
import tempfile

import polars as pl
import kaggle


def stockmarket() -> pl.DataFrame:
    """ Download stock market data from Kaggle

    Returns:
        pl.DataFrame: Raw data
    """

    dfs = []
    # Create temporary directory to download Kaggle data into
    with tempfile.TemporaryDirectory() as tmp_directory:
        # Download kapple dataset

        logging.info("Downloading dataset from Kaggle...")

        kaggle.api.dataset_download_files(
            "jacksoncrow/stock-market-dataset", path=tmp_directory
        )

        zip_path = os.path.join(tmp_directory, "stock-market-dataset.zip")
        # Extract all files in the temporary archive
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmp_directory)

            # Read symbol_valid_meta
            stockmarket_meta_df = pl.read_csv(
                os.path.join(tmp_directory, "symbols_valid_meta.csv")
            )

            for count, file in enumerate(
                glob.glob(os.path.join(tmp_directory, "*/*.csv"))
            ):
                # Read csv (w/ defined dtypes)

                logging.info(f"Reading file: {file}")

                df = pl.read_csv(
                    file,
                    dtypes={
                        "Date": "str",
                        "Open": "f64",
                        "High": "f64",
                        "Low": "f64",
                        "Close": "f64",
                        "Adj Close": "f64",
                        "Volume": "f64",
                    },
                )

                # Preserve metadata about the file being processed
                category = "stock" if "stock" in file else "etf"
                symbol = file.split("/")[-1].split(".")[0]

                # Add symbol and category columns
                df = df.with_columns(
                    pl.lit(symbol).alias("Symbol"), pl.lit(category).alias("Category")
                )

                # Join stock/etf dataframe with stockmarket_meta_df to get Security Name
                df = df.join(
                    stockmarket_meta_df.select(pl.col(["Symbol", "Security Name"])),
                    on="Symbol",
                    how="inner",
                )

                dfs.append(df)

                if count > 3:
                    break

    # Concatenate all dataframes
    data = pl.concat(dfs)

    # Return data
    return data
