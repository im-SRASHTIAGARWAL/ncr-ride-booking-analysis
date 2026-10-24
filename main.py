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

    
    # Generate reports for cancellation and incomplete ride reasons
    reason_columns = {
        "customer_cancellation_reasons": "Reason for cancelling by Customer",
        "driver_cancellation_reasons": "Driver Cancellation Reason",
        "incomplete_ride_reasons": "Incomplete Rides Reason",
    }
    location_report = generate_location_report(df)

    location_path = output_dir / "location_analysis.csv"
    location_report.to_csv(location_path, index=False)

    print("\nTop 10 locations by unsuccessful booking rate:")
    print(location_report.head(10).to_string(index=False))
    print(f"Location report saved to: {location_path}")
    
    for filename, column in reason_columns.items():
        reason_report = generate_reason_report(df, column)

        report_path = output_dir / f"{filename}.csv"
        reason_report.to_csv(report_path, index=False)

        print(f"\nTop reasons for {column}:")
        print(reason_report.head(5).to_string(index=False))
        print(f"Saved to: {report_path}")
        chart_path = save_reason_chart(
        df,
        column,
        f"Top Reasons: {column}",
        f"{filename}.png",
    )
        print(f"Chart saved to: {chart_path}")


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


def generate_reason_report(
    df: pd.DataFrame,
    reason_column: str,
) -> pd.DataFrame:
    """Count the most common reasons in a dataset column."""

    if reason_column not in df.columns:
        raise ValueError(f"Missing required column: {reason_column}")

    reasons = (
        df[reason_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    reasons = reasons[reasons != ""]

    report = (
        reasons.value_counts()
        .rename_axis("Reason")
        .reset_index(name="Count")
    )

    if report.empty:
        report["Percentage"] = pd.Series(dtype=float)
    else:
        report["Percentage"] = (
            report["Count"] / report["Count"].sum() * 100
        ).round(2)

    return report


def generate_location_report(df: pd.DataFrame,minimum_bookings: int = 100,) -> pd.DataFrame:
    """Summarize unsuccessful booking rates by pickup location."""

    required_columns = ["Pickup Location", "Booking Status"]
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if minimum_bookings < 1:
        raise ValueError("minimum_bookings must be at least 1.")

    valid_df = df.dropna(subset=required_columns).copy()

    if valid_df.empty:
        raise ValueError("No valid location data available.")

    unsuccessful_statuses = [
        "Cancelled by Driver",
        "Cancelled by Customer",
        "No Driver Found",
        "Incomplete",
    ]

    valid_df["Unsuccessful"] = (
        valid_df["Booking Status"].isin(unsuccessful_statuses)
    )

    report = (
        valid_df.groupby("Pickup Location")
        .agg(
            Total_Bookings=("Booking Status", "size"),
            Unsuccessful_Bookings=("Unsuccessful", "sum"),
        )
        .reset_index()
    )

    report["Unsuccessful_Rate_Percent"] = (
        report["Unsuccessful_Bookings"]
        / report["Total_Bookings"] * 100
    ).round(2)

    report = report[
        report["Total_Bookings"] >= minimum_bookings
    ]

    return report.sort_values(
        ["Unsuccessful_Rate_Percent", "Total_Bookings"],
        ascending=[False, False],
    )


def save_reason_chart(
    df: pd.DataFrame,
    reason_column: str,
    chart_title: str,
    filename: str,
) -> Path:
    """Create and save a bar chart of ride cancellation reasons."""

    if reason_column not in df.columns:
        raise ValueError(f"Missing required column: {reason_column}")

    reasons = (
        df[reason_column]
        .dropna()
        .astype(str)
        .str.strip()
    )
    reasons = reasons[reasons != ""]

    if reasons.empty:
        raise ValueError(f"No valid reasons found in {reason_column}")

    top_reasons = reasons.value_counts().head(5)

    output_dir = BASE_DIR / "Outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    ax = top_reasons.sort_values().plot(
        kind="barh",
        figsize=(9, 5),
        title=chart_title,
    )
    ax.set_xlabel("Number of Bookings")
    ax.set_ylabel("Reason")

    plt.tight_layout()

    chart_path = output_dir / filename
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close()

    return chart_path


if __name__ == "__main__":
    main()

