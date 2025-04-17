# QuantJourney Trading Calendar

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/quantjourney-calendar.svg)](https://pypi.org/project/quantjourney-calendar/)

A comprehensive trading calendar and exchange management system for financial markets. This library provides essential tools for managing trading hours, holidays, and timezones across multiple exchanges, ensuring accurate time management for trading strategies.

## Features

- **Multi-Exchange Support**: Manage trading schedules for multiple exchanges
- **Accurate Time Management**: Handle timezones and trading hours precisely
- **Holiday Management**: Automatically account for exchange-specific holidays
- **Special Trading Days**: Support for modified trading hours on specific dates
- **Pandas Integration**: Seamless integration with pandas for time series analysis
- **Robust Error Handling**: Comprehensive logging and error management

## Installation

```bash
pip install quantjourney-calendar (in future, now just download repo)
```

Or install from source:

```bash
git clone https://github.com/QuantJourneyOrg/qj_calendar.git
cd qj_calendar
pip install -e .
```

## Quick Start

```python
from trading_calendar import ExchangeInfo, TradingCalendar
import pandas as pd

# Initialize Exchange Information
exchange_info = ExchangeInfo("exchange_calendars/ADX.json")

# Define trading period
start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2024-12-31")

# Create Trading Calendar
trading_calendar = TradingCalendar(exchange_info, start_date, end_date)

# Check if a specific time is trading time
test_time = pd.Timestamp("2024-01-02 11:00:00", tz="Asia/Dubai")
print(trading_calendar.is_trading_time(test_time))  # Output: True or False
```

## Exchange Configuration

Create a JSON file in the `exchange_calendars` directory to define exchange-specific details. Here's an example for ADX (Abu Dhabi Securities Exchange):

```json
{
    "name": "ADX",
    "timezone": "Asia/Dubai",
    "open_time": "10:00",
    "close_time": "14:00",
    "trading_days": [0, 1, 2, 3, 4],  // Monday to Friday
    "holidays": [
        "2024-01-01",  // New Year's Day
        "2024-03-11",  // Ramadan begins
        "2024-04-10",  // Eid al-Fitr
        "2024-06-16",  // Eid al-Adha
        "2024-07-08",  // Islamic New Year
        "2024-12-02"   // UAE National Day
    ],
    "special_trading_days": [
        {
            "date": "2024-07-01",
            "open_time": "10:30",
            "close_time": "13:30"
        }
    ]
}
```

### Adding a New Exchange

1. Create a new JSON file in the `exchange_calendars` directory
2. Follow the structure shown above
3. Include all relevant holidays and special trading days
4. Use the exchange's official timezone
5. Verify trading hours and days according to the exchange's schedule

## API Reference

### ExchangeInfo Class

```python
class ExchangeInfo:
    def __init__(self, json_file_path: str) -> None:
        """Initialize exchange details from JSON file."""
        
    def is_trading_day(self, date: pd.Timestamp) -> bool:
        """Determine if the given date is a trading day."""
        
    def is_holiday(self, date: pd.Timestamp) -> bool:
        """Check if the given date is a holiday."""
        
    def get_trading_hours(self, date: pd.Timestamp) -> Tuple[time, time]:
        """Get trading hours for a specific date."""
```

### TradingCalendar Class

```python
class TradingCalendar:
    def __init__(self, exchange: ExchangeInfo, start_date: pd.Timestamp, 
                 end_date: pd.Timestamp, base_frequency: str = "1D"):
        """Initialize trading calendar for the exchange."""
        
    def is_trading_time(self, timestamp: pd.Timestamp) -> bool:
        """Check if the given timestamp is within trading hours."""
        
    def get_next_trading_time(self, timestamp: pd.Timestamp) -> pd.Timestamp:
        """Get the next available trading time after the given timestamp."""
        
    def get_trading_times(self, start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
        """Retrieve all trading times within the specified period."""
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact jakub@quantjourney.pro.

## Acknowledgments

- Thanks to all contributors who have helped improve this project
- Special thanks to the pandas and pytz communities for their excellent libraries
