from pathlib import Path
import pandas as pd
import pytest

from main import analyze_booking_status, load_data


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
