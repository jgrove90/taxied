import sys
sys.path.insert(0, "./src")
import polars as pl
from utils import write_delta_table, read_delta_table, yaml_vars


DELTA_TABLE_READ_PATH = yaml_vars["bronze_path"]
DELTA_TABLE_SILVER_PATH = yaml_vars["silver_path"]


def silver_taxi_trips_table(table_path: str) -> pl.DataFrame:
    """
    Transforms the silver taxi trips table by adding columns for pickup weekday and pickup hour.

    Args:
        table_path (str): The path to the silver taxi trips table.

    Returns:
        pl.DataFrame: The transformed silver taxi trips table.
    """

    df = read_delta_table(table_path).with_columns(
        pl.col("tpep_pickup_datetime").dt.weekday().alias("pickup_weekday"),
        pl.col("tpep_pickup_datetime").dt.hour().alias("pickup_hour"),
        )
    return df


def main():
    """
    This function is the entry point for the silver transformation process.
    It writes the silver taxi trips table to the specified table path in overwrite mode.
    """
    df = silver_taxi_trips_table(DELTA_TABLE_READ_PATH)
    write_delta_table(df=df, table_path=DELTA_TABLE_SILVER_PATH, mode="overwrite")


if __name__ == "__main__":
    main()
