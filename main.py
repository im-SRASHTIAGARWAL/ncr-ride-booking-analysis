from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def save_booking_status_chart(df: pd.DataFrame) -> Path:
    """Create and save a chart of booking statuses."""
    if "Booking Status" not in df.columns:
        raise ValueError("Missing 'Booking Status' column.")

    output_dir = BASE_DIR / "outputs"
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


def analyze_booking_status(df: pd.DataFrame) -> pd.Series:
    """Count bookings by status."""
    if "Booking Status" not in df.columns:
        raise ValueError("Missing 'Booking Status' column.")

    return df["Booking Status"].value_counts()



def main() -> None:
    df = load_data(DATA_PATH)

    print(f"Dataset loaded successfully: {len(df):,} rows")
    print("\nBookings by status:")
    print(analyze_booking_status(df))

    chart_path = save_booking_status_chart(df)
    print(f"\nChart saved to: {chart_path}")


if __name__ == "__main__":
    main()
