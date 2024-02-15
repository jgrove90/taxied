import sys
sys.path.insert(0, "./src")
from utils import get_parquet_data, write_delta_table, yaml_vars

SOURCE_DATA = yaml_vars["taxi_source_data"]
DELTA_PATH_BRONZE = yaml_vars["bronze_path"]


def main():
    """
    This function is the entry point for the bronze transformation process.
    It writes the taxi source data to the specified table path in overwrite mode.
    """
    df = get_parquet_data(SOURCE_DATA)
    write_delta_table(df=df, table_path=DELTA_PATH_BRONZE, mode="overwrite")


if __name__ == "__main__":
    main()
