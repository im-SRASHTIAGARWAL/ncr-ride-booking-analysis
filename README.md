# NCR Ride Booking Analysis

A Python-based data analysis project that explores ride booking patterns, booking cancellations, incomplete rides, and cancellation reasons using NCR ride booking data.

## Project Overview

The project processes ride booking data using Pandas, validates the dataset, generates summary reports, and creates visualizations to identify common booking outcomes and unsuccessful ride patterns.

## Features

- **Data Loading:** Loads the ride booking CSV dataset.
- **Data Validation:** Checks required columns and essential booking fields.
- **Booking Analysis:** Summarizes bookings by status and calculates percentages.
- **Cancellation Analysis:** Reports driver cancellations, customer cancellations, rides with no driver found, and incomplete rides.
- **Reason Analysis:** Identifies frequently reported customer cancellation, driver cancellation, and incomplete ride reasons.
- **Visualizations:** Generates booking status and reason-based bar charts.
- **CSV Reports:** Saves analysis results for further inspection.
- **Automated Testing:** Uses pytest to verify core functions and error handling.

## Technologies Used

- Python
- Pandas
- Matplotlib
- Pytest
- Git and GitHub

## Project Structure

```text
Uber_data_analysis/
├── data/
│   └── ncr_ride_bookings.csv
├── Outputs/
│   ├── booking_status.png
│   ├── booking_summary.csv
│   ├── cancellation_report.csv
│   ├── customer_cancellation_reasons.csv
│   ├── driver_cancellation_reasons.csv
│   └── incomplete_ride_reasons.csv
├── main.py
├── test_analysis.py
├── requirements.txt
├── .gitignore
└── README.md
```

*Generated chart files are also saved in the `Outputs/` directory. The dataset and virtual environment are excluded from version control.*

## Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/im-SRASHTIAGARWAL/ncr-ride-booking-analysis.git
   cd ncr-ride-booking-analysis
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Place the dataset at:

   ```text
   data/ncr_ride_bookings.csv
   ```

   The dataset is not included in this repository. Use a dataset you are permitted to access and redistribute or keep locally.

5. Run the analysis:

   ```bash
   python main.py
   ```

6. Run automated tests:

   ```bash
   python -m pytest -v
   ```

## Outputs

The project generates:

- `booking_summary.csv` — booking counts and percentages by status.
- `cancellation_report.csv` — unsuccessful booking counts and percentages.
- `customer_cancellation_reasons.csv` — customer cancellation reason counts.
- `driver_cancellation_reasons.csv` — driver cancellation reason counts.
- `incomplete_ride_reasons.csv` — incomplete ride reason counts.
- PNG charts for booking status and the three reason categories.

## Visualizations

### 1. Booking Status Distribution
![Booking Status Distribution](Docs/images/booking_status.png)

### 2. Customer Cancellation Reasons
![Customer Cancellation Reasons](Docs/images/customer_cancellation_reasons.png)

### 3. Driver Cancellation Reasons
![Driver Cancellation Reasons](Docs/images/driver_cancellation_reasons.png)

### 4. Incomplete Ride Reasons
![Incomplete Ride Reasons](Docs/images/incomplete_ride_reasons.png)

### 5. Locations with Highest Unsuccessful Booking Rates
![Location Analysis](Docs/images/location_unsuccessful_rate.png)

## Key Findings

In the analyzed dataset of 150,000 bookings:

- 93,000 bookings (62%) were completed.
- 27,000 bookings (18%) were cancelled by drivers.
- 10,500 bookings (7%) were cancelled by customers.
- 10,500 bookings (7%) had no driver found.
- 9,000 bookings (6%) were marked incomplete.

These are descriptive findings from the analyzed dataset and do not establish the causes of cancellations.

## Testing

Core functionality is tested using pytest, including booking status counts, data validation, missing-file handling, report calculations, and cancellation reason analysis.

## Future Improvements

- Add more detailed location-based analysis.
- Build an interactive dashboard.
- Add further data quality and edge-case tests.
- Explore trends across dates, time periods, and vehicle types.

## Author

**Srashti Agarwal**

GitHub: [im-SRASHTIAGARWAL](https://github.com/im-SRASHTIAGARWAL)
