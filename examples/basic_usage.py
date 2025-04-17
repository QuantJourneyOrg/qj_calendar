"""
    Basic usage example of the QuantJourney Trading Calendar.
    This script demonstrates how to:
    1. Initialize an exchange calendar
    2. Check trading times
    3. Get next trading time
    4. Get trading times within a period
"""

import pandas as pd
from calendar.trading_calendar import ExchangeInfo, TradingCalendar

def main():
    # Initialize Exchange Information
    print("Initializing ADX exchange information...")
    exchange_info = ExchangeInfo("calendar/exchange_calendars/ADX.json")
    
    # Define trading period
    start_date = pd.Timestamp("2024-01-01")
    end_date = pd.Timestamp("2024-01-31")
    
    # Create Trading Calendar
    print(f"\nCreating trading calendar for period {start_date} to {end_date}...")
    trading_calendar = TradingCalendar(exchange_info, start_date, end_date)
    
    # Example 1: Check if a specific time is trading time
    test_time = pd.Timestamp("2024-01-02 11:00:00", tz="Asia/Dubai")
    is_trading = trading_calendar.is_trading_time(test_time)
    print(f"\nExample 1: Is {test_time} a trading time? {is_trading}")
    
    # Example 2: Get next trading time
    test_time = pd.Timestamp("2024-01-01 15:00:00", tz="Asia/Dubai")  # After market close
    next_trading = trading_calendar.get_next_trading_time(test_time)
    print(f"\nExample 2: Next trading time after {test_time} is {next_trading}")
    
    # Example 3: Get trading times for a specific day
    day_start = pd.Timestamp("2024-01-03", tz="Asia/Dubai")
    day_end = pd.Timestamp("2024-01-04", tz="Asia/Dubai")
    trading_times = trading_calendar.get_trading_times(day_start, day_end)
    print(f"\nExample 3: Trading times for {day_start.date()}:")
    print(trading_times)
    
    # Example 4: Check holiday
    holiday = pd.Timestamp("2024-01-01", tz="Asia/Dubai")
    is_holiday = exchange_info.is_holiday(holiday)
    print(f"\nExample 4: Is {holiday.date()} a holiday? {is_holiday}")

if __name__ == "__main__":
    main() 