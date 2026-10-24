from pathlib import Path
import pandas as pd
import pytest
from main import generate_booking_report, generate_cancellation_report, generate_location_report, generate_reason_report
from main import analyze_booking_status, load_data

def test_generate_booking_report_percentages():
    df = pd.DataFrame({
        "Booking Status": [
            "Completed",
            "Completed",
            "Cancelled by Customer",
            "Incomplete",
        ]
    })

    report = generate_booking_report(df)
    percentages = dict(
        zip(report["Booking Status"], report["Percentage"])
    )

    assert percentages["Completed"] == 50.0
    assert percentages["Cancelled by Customer"] == 25.0
    assert percentages["Incomplete"] == 25.0


def test_generate_booking_report_rejects_empty_data():
    df = pd.DataFrame({"Booking Status": []})

    with pytest.raises(ValueError, match="empty dataset"):
        generate_booking_report(df)

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


def test_cancellation_report_percentages():
    df = pd.DataFrame({
        "Booking Status": [
            "Completed",
            "Cancelled by Driver",
            "Cancelled by Customer",
            "No Driver Found",
            "Incomplete",
        ]
    })

    report = generate_cancellation_report(df)

    assert list(report["Bookings"]) == [1, 1, 1, 1]
    assert list(report["Percentage"]) == [20.0, 20.0, 20.0, 20.0]

def test_generate_reason_report():
    df = pd.DataFrame({
        "Reason": [
            "Wrong Address",
            "Wrong Address",
            "Change of plans",
            None,
            "",
        ]
    })

    report = generate_reason_report(df, "Reason")

    assert report.iloc[0]["Reason"] == "Wrong Address"
    assert report.iloc[0]["Count"] == 2
    assert report.iloc[0]["Percentage"] == 66.67

def test_generate_location_report():
    df = pd.DataFrame({
        "Pickup Location": ["A", "A", "A", "B", "B"],
        "Booking Status": [
            "Completed",
            "Cancelled by Driver",
            "Completed",
            "No Driver Found",
            "Completed",
        ],
    })

    """report = generate_location_report(df)"""
    report = generate_location_report(df, minimum_bookings=1)
    report = report.set_index("Pickup Location")

    assert report.loc["A", "Total_Bookings"] == 3
    assert report.loc["A", "Unsuccessful_Bookings"] == 1
    assert report.loc["A", "Unsuccessful_Rate_Percent"] == 33.33

    assert report.loc["B", "Total_Bookings"] == 2
    assert report.loc["B", "Unsuccessful_Bookings"] == 1
    assert report.loc["B", "Unsuccessful_Rate_Percent"] == 50.0


def test_location_report_filters_low_booking_counts():
    df = pd.DataFrame({
        "Pickup Location": ["A"] * 3 + ["B"] * 101,
        "Booking Status": (
            ["Completed"] * 2
            + ["Cancelled by Driver"]
            + ["Completed"] * 80
            + ["Cancelled by Driver"] * 21
        ),
    })

    report = generate_location_report(df, minimum_bookings=100)

    assert "A" not in report["Pickup Location"].values
    assert "B" in report["Pickup Location"].values
