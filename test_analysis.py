from pathlib import Path
import pandas as pd
import pytest

from main import analyze_booking_status, load_data

from main import validate_data
def test_validate_data_accepts_valid_dataset():
    df = pd.DataFrame({
        "Booking ID": ["B1", "B2"],
        "Booking Status": ["Completed", "Incomplete"],
        "Vehicle Type": ["Auto", "Bike"],
        "Pickup Location": ["Noida", "Delhi"],
        "Booking Value": [250.0,None],
    })

    validate_data(df)
def test_validate_data_rejects_missing_column():
    df = pd.DataFrame({
        "Booking ID": ["B1"],
        "Booking Status": ["Completed"],
    })

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_data(df)


def test_validate_data_rejects_missing_booking_id():
    df = pd.DataFrame({
        "Booking ID": [None],
        "Booking Status": ["Completed"],
        "Vehicle Type": ["Auto"],
        "Pickup Location": ["Noida"],
        "Booking Value": [250.0],
    })

    with pytest.raises(ValueError, match="Booking ID"):
        validate_data(df)


def test_analyze_booking_status_counts():
    df = pd.DataFrame({
        "Booking Status": [
            "Completed",
            "Completed",
            "Cancelled by Customer",
        ]
    })

    result = analyze_booking_status(df)

    assert result["Completed"] == 2
    assert result["Cancelled by Customer"] == 1


def test_missing_booking_status_column():
    df = pd.DataFrame({"Customer ID": ["C1", "C2"]})

    with pytest.raises(ValueError, match="Booking Status"):
        analyze_booking_status(df)


def test_missing_dataset_file():
    missing_path = Path("this_file_does_not_exist.csv")

    with pytest.raises(FileNotFoundError):
        load_data(missing_path)
