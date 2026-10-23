from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def save_booking_status_chart(df: pd.DataFrame) -> Path:
    """Create and save a chart of booking statuses."""
    if "Booking Status" not in df.columns:
        raise ValueError("Missing 'Booking Status' column.")
    output_dir = BASE_DIR / "Outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    status_counts = df["Booking Status"].value_counts()

    ax = status_counts.plot(
        kind="bar",
        figsize=(10, 5),
        title="Ride Booking Status Distribution"
    )
    ax.set_xlabel("Booking Status")
    ax.set_ylabel("Number of Bookings")

    plt.tight_layout()

    chart_path = output_dir / "booking_status.png"
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close()

    return chart_path

# Project folder location
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "ncr_ride_bookings.csv"


def load_data(file_path: Path) -> pd.DataFrame:
    """Load ride booking data from a CSV file."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("The dataset is empty.")

    return df


REQUIRED_COLUMNS = [
    "Booking ID",
    "Booking Status",
    "Vehicle Type",
    "Pickup Location",
    "Booking Value",
]


def validate_data(df: pd.DataFrame) -> None:
    """Validate required columns and dataset contents."""
    if df.empty:
        raise ValueError("The dataset is empty.")

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df["Booking ID"].isna().any():
        raise ValueError("Booking ID contains missing values.")

    if df["Booking Status"].isna().any():
        raise ValueError("Booking Status contains missing values.")

    if df["Vehicle Type"].isna().any():
        raise ValueError("Vehicle Type contains missing values.")

    if df["Pickup Location"].isna().any():
        raise ValueError("Pickup Location contains missing values.")

def analyze_booking_status(df: pd.DataFrame) -> pd.Series:
    """Count bookings by status."""
    if "Booking Status" not in df.columns:
        raise ValueError("Missing 'Booking Status' column.")

    return df["Booking Status"].value_counts()



def generate_booking_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a summary report for booking statuses."""

    total_bookings = len(df)

    if total_bookings == 0:
        raise ValueError("Cannot report on an empty dataset.")

    status_counts = df["Booking Status"].value_counts()

    report = pd.DataFrame({
        "Booking Status": status_counts.index,
        "Bookings": status_counts.values,
    })

    report["Percentage"] = (
        report["Bookings"] / total_bookings * 100
    ).round(2)

    return report


def main() -> None:
    df = load_data(DATA_PATH)
    validate_data(df)

    output_dir = BASE_DIR / "Outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate and save the complete booking summary
    report = generate_booking_report(df)
    report_path = output_dir / "booking_summary.csv"
    report.to_csv(report_path, index=False)

    # Generate and save the unsuccessful booking report
    cancellation_report = generate_cancellation_report(df)
    cancellation_path = output_dir / "cancellation_report.csv"
    cancellation_report.to_csv(cancellation_path, index=False)

    print(f"Dataset loaded and validated: {len(df):,} rows")
    print("\nBookings by status:")
    print(report.to_string(index=False))

    print("\nCancellation and unsuccessful booking report:")
    print(cancellation_report.to_string(index=False))

    chart_path = save_booking_status_chart(df)
    print(f"\nBooking report saved to: {report_path}")
    print(f"Cancellation report saved to: {cancellation_path}")
    print(f"Chart saved to: {chart_path}")




def generate_cancellation_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a report of unsuccessful bookings."""

    unsuccessful_statuses = [
        "Cancelled by Driver",
        "Cancelled by Customer",
        "No Driver Found",
        "Incomplete",
    ]

    total_bookings = len(df)

    status_counts = df["Booking Status"].value_counts()

    report = pd.DataFrame({
        "Booking Status": unsuccessful_statuses,
        "Bookings": [
            int(status_counts.get(status, 0))
            for status in unsuccessful_statuses
        ],
    })

    report["Percentage"] = (
        report["Bookings"] / total_bookings * 100
    ).round(2)

    return report


if __name__ == "__main__":
    main()

