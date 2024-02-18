import sys
import tempfile

sys.path.insert(0, "./src")
import polars as pl
from transformations.silver.silver_taxi_trips_table import silver_taxi_trips_table
import pytest
from datetime import datetime


@pytest.fixture
def sample_table_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield f"{temp_dir}/silver_taxi_trips_table"


def test_silver_taxi_trips_table(sample_table_path):
    # Generate sample data
    data = {
        "tpep_pickup_datetime": [
            datetime.strptime("2022-01-01 08:30:00", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2022-01-02 12:45:00", "%Y-%m-%d %H:%M:%S"),
        ],
    }
    df = pl.DataFrame(data)

    # Save sample data as delta table
    df.write_delta(sample_table_path)

    # Call the function under test
    result = silver_taxi_trips_table(sample_table_path)

    # Assert the expected columns are present
    assert "pickup_weekday" in result.columns
    assert "pickup_hour" in result.columns

    # Assert the expected values in the transformed columns
    assert result["pickup_weekday"].to_list() == [6, 7]  # Saturday, Sunday
    assert result["pickup_hour"].to_list() == [8, 12]

