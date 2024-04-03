import polars as pl
import yaml


def get_parquet_data(url: str) -> pl.DataFrame:
    """
    Reads a Parquet file from the given URL and returns a DataFrame.

    Parameters:
        url (str): The URL of the Parquet file.

    Returns:
        DataFrame: The DataFrame containing the data from the Parquet file.
    """
    print(f"Retrieving parquet file from {url}")
    df = pl.read_parquet(url)
    return df


def write_delta_table(df: pl.DataFrame, table_path: str, mode: str) -> None:
    """
    Writes a DataFrame to a Delta table.

    Args:
        df (pl.DataFrame): The DataFrame to write.
        table_path (str): The path to the Delta table.
        mode (str): The write mode. Possible values are 'overwrite', 'append', and 'ignore'.
        storage_options (dict): The storage options for the Delta table.

    Returns:
        None
    """
    print(f"Writing Delta table to {table_path} in '{mode}' mode")
    storage_options = {'AWS_S3_LOCKING_PROVIDER': 'dynamodb', 
                       'DELTA_DYNAMO_TABLE_NAME': 'delta_log'}
    df.write_delta(table_path, mode=mode, storage_options=storage_options)
    return None


def read_delta_table(table_path: str) -> pl.DataFrame:
    """
    Read a Delta table from the specified path.

    Args:
        table_path (str): The path to the Delta table.

    Returns:
        pl.DataFrame: The DataFrame representing the Delta table.
    """
    print(f"Reading Delta table from {table_path}")
    df = pl.read_delta(table_path)
    return df


with open("src/config.yaml", "r") as file:
    yaml_vars = yaml.safe_load(file)
