"""
QuantJourney Trading Calendar Package

A comprehensive trading calendar and exchange management system for financial markets.
This package provides essential tools for managing trading hours, holidays, and timezones
across multiple exchanges, ensuring accurate time management for trading strategies.

Example:
    >>> from calendar import ExchangeInfo, TradingCalendar
    >>> import pandas as pd
    >>> 
    >>> # Initialize exchange
    >>> exchange = ExchangeInfo("calendar/exchange_calendars/ADX.json")
    >>> 
    >>> # Create calendar
    >>> start_date = pd.Timestamp("2024-01-01")
    >>> end_date = pd.Timestamp("2024-12-31")
    >>> calendar = TradingCalendar(exchange, start_date, end_date)
"""

from .trading_calendar import ExchangeInfo, TradingCalendar

__version__ = "0.1.0"
__all__ = ["ExchangeInfo", "TradingCalendar"]
