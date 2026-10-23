# NCR Ride Booking Data Analysis

## Overview

A Python-based data analysis project that examines ride-booking outcomes across NCR pickup locations and vehicle types. The project explores booking statuses, customer and driver cancellations, incomplete rides, and driver availability.

## Features

- Load and validate ride-booking CSV data.
- Summarize bookings by status.
- Analyze cancellation and driver-availability patterns.
- Generate and save booking-status charts.
- Run automated tests with pytest.

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- pytest

## Setup

1. Clone or download this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Place the permitted dataset at `data/ncr_ride_bookings.csv`.
5. Run the analysis:

   `python main.py`

6. Run tests:

   `python -m pytest -v`

## Initial Findings

In the analysed dataset of 150,000 bookings:

- 93,000 bookings were completed (62%).
- 27,000 were cancelled by drivers (18%).
- 10,500 were cancelled by customers (7%).
- 10,500 had no driver found (7%).
- 9,000 were incomplete (6%).

The initial location analysis showed a 38.88% combined rate of customer cancellations, driver cancellations, and no-driver-found outcomes in Vinobapuri among the locations examined. These are descriptive findings and do not establish the causes of cancellations.

## Data and Limitations

The dataset is not included in this repository by default. Add it locally as `data/ncr_ride_bookings.csv` only after verifying that its licence permits redistribution. Missing booking values for cancelled bookings are not assumed to represent zero revenue.

## Testing

Automated tests cover booking-status counts, missing required columns, and missing dataset files.

## Future Improvements

- Add further data-quality checks.
- Analyse cancellation reasons and vehicle-type patterns.
- Expand automated test coverage.
- Add configurable report generation.
