# QuantJourney Calendar and Exchange Management

## Overview

The QuantJourney Calendar and Exchange Management module provides essential tools for managing trading hours, holidays, and timezones across multiple exchanges. Primarily used in backtesting and live trading environments, it ensures accurate time management and synchronization for trading strategies operating on different exchanges with varying schedules.

## Quick Start

```python
from quantjourney.calendar import ExchangeInfo, TradingCalendar
import pandas as pd

# Initialize Exchange Information
exchange_info = ExchangeInfo("./quantjourney/calendars/exchange_calendars/DFM.json")

# Define trading period
start_date = pd.Timestamp("2023-01-01")
end_date = pd.Timestamp("2023-12-31")

# Create Trading Calendar
trading_calendar = TradingCalendar(exchange_info, start_date, end_date)

# Check if a specific time is trading time
test_time = pd.Timestamp("2023-01-02 11:00:00", tz="Asia/Dubai")
print(trading_calendar.is_trading_time(test_time))  # Output: True or False

# Get next trading time after a given timestamp
next_trading_time = trading_calendar.get_next_trading_time(test_time)
print(next_trading_time)
```

## Example Exchange Configuration

Create a JSON file (e.g., `DFM.json`) with the following structure to define exchange-specific details:

```json5
{
    "name": "DFM",
    "timezone": "Asia/Dubai",
    "open_time": "10:00",
    "close_time": "14:00",
    "trading_days": [6, 0, 1, 2, 3],  // 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    "holidays": [
        "2014-01-01",  // New Year's Day
        "2014-05-27",  // Isra and Mi'raj
        "2014-07-29",  // Eid al-Fitr
        "2014-10-04",  // Arafat (Haj) Day
        "2014-10-05",  // Eid al-Adha
        "2014-10-25",  // Hijri New Year
        "2014-12-02",  // UAE National Day
        // Add more holidays as needed
    ],
    "special_trading_days": [
        {
            "date": "2024-07-01",
            "open_time": "10:30",
            "close_time": "13:30"
        }
        // Add more special trading days as needed
    ]
}
```

## Architecture

```
calendar/
├── __init__.py             # Package initialization and exports
├── exchange.py             # ExchangeInfo and TradingCalendar classes
├── holidays.py             # Holiday management utilities
├── decorators.py           # Decorators for error logging
└── exchange_calendars/
    └── DFM.json            # Example exchange configuration
```

1. **ExchangeInfo Class**

```python
class ExchangeInfo:
    def __init__(self, json_file_path: str) -> None:
        # Initialize exchange details from JSON file

    def is_trading_day(self, date: pd.Timestamp) -> bool:
        # Determine if the given date is a trading day

    def is_holiday(self, date: pd.Timestamp) -> bool:
        # Check if the given date is a holiday

    def get_trading_hours(self, date: pd.Timestamp) -> Tuple[time, time]:
        # Get trading hours for a specific date
```

2. **TradingCalendar Class**

```python
class TradingCalendar:
    def __init__(self, exchange: ExchangeInfo, start_date: pd.Timestamp, end_date: pd.Timestamp, base_frequency: str = "1D"):
        # Initialize trading calendar for the exchange

    def is_trading_time(self, timestamp: pd.Timestamp) -> bool:
        # Check if the given timestamp is within trading hours

    def get_next_trading_time(self, timestamp: pd.Timestamp) -> pd.Timestamp:
        # Get the next available trading time after the given timestamp

    def get_trading_times(self, start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
        # Retrieve all trading times within the specified period

    def reset(self, start_date: Optional[pd.Timestamp] = None, end_date: Optional[pd.Timestamp] = None):
        # Reset the trading calendar with new dates

    def step(self):
        # Advance the calendar by one step

    def get_current_time(self) -> pd.Timestamp:
        # Get the current timestamp in the calendar

    def is_finished(self) -> bool:
        # Check if the calendar has reached the end date

    def get_exchange_trading_hours(self) -> Tuple[time, time]:
        # Get the exchange's standard trading hours

    def get_exchange_timezone(self) -> timezone:
        # Get the exchange's timezone
```

## Features

### 1. Comprehensive Trading Time Management

- **Trading Hours**: Define and manage opening and closing times for each exchange.
- **Holidays**: Automatically account for exchange-specific holidays to prevent trading on non-operational days.
- **Special Trading Days**: Handle days with modified trading hours.
- **Timezones**: Handle multiple timezones seamlessly, ensuring accurate time calculations across different regions.

### 2. Multi-Exchange Support

- **Simultaneous Management**: Manage trading schedules for multiple exchanges with differing hours and holidays.
- **Scalability**: Easily add new exchanges by providing their configuration in JSON format.

### 3. Integration with Backtesting and Live Trading

- **Backtesting**: Ensure that historical data aligns with actual trading hours and holidays for accurate strategy testing.
- **Live Trading**: Maintain synchronization with exchange schedules to execute trades precisely during operational hours.

### 4. Error Handling and Logging

- **Robust Logging**: Utilize the QuantJourney logging system to capture and log errors during calendar operations.
- **Decorators**: Implement decorators to streamline error logging and handling within classes.

## Usage

### Initializing Exchange Information

```python
from quantjourney.calendar import ExchangeInfo

exchange_info = ExchangeInfo("./quantjourney/calendars/exchange_calendars/DFM.json")
```

### Creating a Trading Calendar

```python
from quantjourney.calendar import TradingCalendar
import pandas as pd

start_date = pd.Timestamp("2023-01-01")
end_date = pd.Timestamp("2023-12-31")

trading_calendar = TradingCalendar(exchange_info, start_date, end_date)
```

### Checking Trading Time

```python
test_time = pd.Timestamp("2023-01-02 11:00:00", tz="Asia/Dubai")
is_trading = trading_calendar.is_trading_time(test_time)
print(is_trading)  # Output: True or False
```

### Retrieving Next Trading Time

```python
next_trading_time = trading_calendar.get_next_trading_time(test_time)
print(next_trading_time)
```

### Getting Trading Times Within a Period

```python
test_start = pd.Timestamp("2023-01-05", tz="Asia/Dubai")
test_end = pd.Timestamp("2023-01-06", tz="Asia/Dubai")
testing_times = trading_calendar.get_trading_times(test_start, test_end)
print(trading_times)
```

### Resetting the Trading Calendar

```python
trading_calendar.reset(start_date=pd.Timestamp("2024-01-01"), end_date=pd.Timestamp("2024-12-31"))
```

### Stepping Through the Calendar

```python
while not trading_calendar.is_finished():
    current_time = trading_calendar.get_current_time()
    print(current_time)
    trading_calendar.step()
```

## Configuration

### Environment Variables

- `BASE_DIR`: Set the base directory for exchange configurations (default: `quantjourney`)

### Exchange Configuration Files

Define each exchange in a separate JSON file within the `exchange_calendars` directory. Each file should include:

- `name`: Name of the exchange
- `timezone`: Timezone of the exchange
- `open_time`: Opening time (HH:MM format)
- `close_time`: Closing time (HH:MM format)
- `trading_days`: List of trading days (0=Monday, ..., 6=Sunday)
- `holidays`: List of holiday dates (`YYYY-MM-DD` format)
- `special_trading_days`: List of special trading days with modified hours

## Best Practices

**Use Structured Configuration Files**

```json5
{
    "name": "DFM",
    "timezone": "Asia/Dubai",
    "open_time": "10:00",
    "close_time": "14:00",
    "trading_days": [6, 0, 1, 2, 3],  // 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    "holidays": [
        "2024-01-01",  // New Year's Day
        "2024-02-08",  // Isra and Mi'raj
        "2024-04-11",  // Eid al-Fitr
        "2024-06-15",  // Arafat (Haj) Day
        "2024-06-16",  // Eid al-Adha
        "2024-07-07",  // Hijri New Year
        "2024-12-02"   // UAE National Day
    ],
    "special_trading_days": [
        {
            "date": "2024-07-01",
            "open_time": "10:30",
            "close_time": "13:30"
        }
        // Add more special trading days as needed
    ]
}
```

**Handle Multiple Timezones Carefully**

Ensure that all timestamps are timezone-aware to prevent discrepancies in trading operations.

**Integrate with the Logging System**

Utilize the QuantJourney logging system to monitor and debug calendar-related operations effectively.

## Unit Testing

### Running Unit Tests

The module includes a set of unit tests to verify its functionality. To run the tests, execute the main script:

```bash
python calendar_module.py
```

### Example Output

```plaintext
--- Running unit test: CREATE_CALENDAR ---
Calendar created:
                         is_trading_time
2023-01-05 10:00:00+04:00               True
2023-01-05 11:00:00+04:00               True
...
2023-12-31 13:00:00+04:00               True
2023-12-31 14:00:00+04:00              False

--- Running unit test: IS_TRADING_TIME ---
Is trading time for NYSE at 2023-01-05 10:00:00+04:00:
True

--- Running unit test: GET_NEXT_TRADING_TIME ---
Next trading time after 2023-01-02 16:01:00+05:00:
2023-01-03 10:00:00+05:00

--- Running unit test: GET_TRADING_TIMES ---
Trading times between 2023-01-05 00:00:00+04:00 and 2023-01-06 00:00:00+04:00:
DatetimeIndex(['2023-01-05 10:00:00+04:00', '2023-01-05 11:00:00+04:00',
               '2023-01-05 12:00:00+04:00', '2023-01-05 13:00:00+04:00'],
              dtype='datetime64[ns, Asia/Dubai]', freq=None)

--- Running unit test: GET_EXCHANGE_TRADING_HOURS ---
DFM trading hours:
(datetime.time(10, 0), datetime.time(14, 0))

```

## Troubleshooting

Common issues and solutions:

1. **Incorrect Trading Times**
   - Verify the exchange configuration JSON for accurate `open_time` and `close_time`.
   - Ensure timezone settings match the exchange's local timezone.

2. **Holidays Not Recognized**
   - Confirm holiday dates are correctly formatted (`YYYY-MM-DD`).
   - Check if holidays overlap with trading days.

3. **Time Zone Mismatch**
   - Ensure all timestamps are timezone-aware.
   - Verify the `timezone` field in the exchange configuration.

4. **Special Trading Days Not Applied**
   - Ensure `special_trading_days` are correctly defined in the JSON configuration.
   - Verify the dates and times are accurately specified.

## Security

- **Data Protection**: Ensure exchange configuration files are secured and access-controlled.
- **Compliance**: Adhere to relevant financial regulations regarding trading operations and data management.

## License

Proprietary - QuantJourney Framework

This file is part of the QuantJourney Framework and is licensed for internal, non-commercial use only.
Modifications are permitted solely for personal, non-commercial testing. Redistribution and commercial use are prohibited.

For full terms, see the LICENSE file or contact Jakub Polec at jakub@quantjourney.pro.
