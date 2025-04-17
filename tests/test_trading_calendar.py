"""
Test suite for the QuantJourney Trading Calendar package.
"""

import pytest
import pandas as pd
from calendar import ExchangeInfo, TradingCalendar

@pytest.fixture
def adx_exchange():
    """Fixture providing ADX exchange information."""
    return ExchangeInfo("calendar/exchange_calendars/ADX.json")

@pytest.fixture
def trading_calendar(adx_exchange):
    """Fixture providing a trading calendar instance."""
    start_date = pd.Timestamp("2024-01-01")
    end_date = pd.Timestamp("2024-01-31")
    return TradingCalendar(adx_exchange, start_date, end_date)

def test_exchange_info_initialization(adx_exchange):
    """Test ExchangeInfo initialization and attributes."""
    assert adx_exchange.name == "ADX"
    assert adx_exchange.timezone.zone == "Asia/Dubai"
    assert adx_exchange.open_time.hour == 10
    assert adx_exchange.close_time.hour == 14

def test_trading_day_check(adx_exchange):
    """Test trading day verification."""
    # Regular trading day
    trading_day = pd.Timestamp("2024-01-02", tz="Asia/Dubai")
    assert adx_exchange.is_trading_day(trading_day)
    
    # Weekend
    weekend = pd.Timestamp("2024-01-06", tz="Asia/Dubai")  # Saturday
    assert not adx_exchange.is_trading_day(weekend)
    
    # Holiday
    holiday = pd.Timestamp("2024-01-01", tz="Asia/Dubai")  # New Year's Day
    assert not adx_exchange.is_trading_day(holiday)

def test_trading_time_check(trading_calendar):
    """Test trading time verification."""
    # During trading hours
    trading_time = pd.Timestamp("2024-01-02 11:00:00", tz="Asia/Dubai")
    assert trading_calendar.is_trading_time(trading_time)
    
    # Outside trading hours
    non_trading_time = pd.Timestamp("2024-01-02 15:00:00", tz="Asia/Dubai")
    assert not trading_calendar.is_trading_time(non_trading_time)

def test_next_trading_time(trading_calendar):
    """Test next trading time calculation."""
    # After market close
    after_close = pd.Timestamp("2024-01-02 15:00:00", tz="Asia/Dubai")
    next_trading = trading_calendar.get_next_trading_time(after_close)
    assert next_trading.date() == pd.Timestamp("2024-01-03").date()
    assert next_trading.hour == 10  # Market open time

def test_trading_times_range(trading_calendar):
    """Test getting trading times within a range."""
    start = pd.Timestamp("2024-01-03", tz="Asia/Dubai")
    end = pd.Timestamp("2024-01-04", tz="Asia/Dubai")
    trading_times = trading_calendar.get_trading_times(start, end)
    
    # Should include all hours between open and close
    assert len(trading_times) == 4  # 10:00, 11:00, 12:00, 13:00
    assert trading_times[0].hour == 10
    assert trading_times[-1].hour == 13

def test_special_trading_day(adx_exchange):
    """Test special trading day handling."""
    special_day = pd.Timestamp("2024-07-01", tz="Asia/Dubai")
    open_time, close_time = adx_exchange.get_trading_hours(special_day)
    assert open_time.hour == 10
    assert open_time.minute == 30
    assert close_time.hour == 13
    assert close_time.minute == 30 