"""
	Calendar and Exchange classes for trading time management
    ---------------------------------------------------------

	Used mostly in Backtesting and Trading environments to manage trading hours, holidays, and timezones.
	You could use this class to manage trading hours, holidays, and timezones in your trading environment.
	And backtest / trade on multiple exchanges with different trading hours and holidays same time.

	date: 2024-11-15

    Note:
    This module is part of a larger educational and prototyping framework and may lack
    advanced features or optimizations found in production-grade systems.

    Proprietary License - QuantJourney Framework
    This file is part of the QuantJourney Framework and is licensed for internal, non-commercial use only.
    Modifications are permitted solely for personal, non-commercial testing. Redistribution and commercial use are prohibited.

    For full terms, see the LICENSE file or contact Jakub Polec at jakub@quantjourney.pro.
"""

import pandas as pd
from typing import Dict, Tuple, Optional
from pytz import timezone
from datetime import time, datetime
from pytz import timezone as pytz_timezone
from enum import Enum
import asyncio
import json5 as json  # JSON5 is a superset of JSON that allows comments and trailing commas

from quantjourney.other.decorators import error_logger
from quantjourney.logger import logger


# ExchangeInfo class ----------------------------------------------------------
class ExchangeInfo:
    def __init__(
        self,
        json_file_path: str
    ) -> None:
        """
        Class for managing information about an exchange

        Atributes:
                name (str): Name of the exchange
                timezone (timezone): Timezone of the exchange
                open_time (time): Opening time of the exchange
                close_time (time): Closing time of the exchange
                trading_days (List[int]): List of trading days (0=Monday, 1=Tuesday, ..., 6=Sunday)
                holidays (List[datetime.date]): List of holidays
                special_trading_days (List[Dict[str, str]]): List of special trading days with open and close times
        """
        try:
            with open(json_file_path, "r") as file:
                data = json.load(file)
            logger.info(f"Loaded exchange info from {json_file_path}")
        except Exception as e:
            logger.error(f"Error loading exchange info from {json_file_path}: {e}")
            raise

        # Required fields
        required_fields = [
            "name",
            "timezone",
            "open_time",
            "close_time",
            "trading_days",
            "holidays",
        ]
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                raise

        self.name = data["name"]
        self.timezone = pytz_timezone(data["timezone"])
        self.open_time = datetime.strptime(data["open_time"], "%H:%M").time()
        self.close_time = datetime.strptime(data["close_time"], "%H:%M").time()
        self.trading_days = data["trading_days"]
        self.holidays = [
            datetime.strptime(date, "%Y-%m-%d").date() for date in data["holidays"]
        ]
        self.special_trading_days = data.get("special_trading_days", [])

        # Optional: Load holiday calendar if specified in JSON
        self.holiday_calendar = None
        if "holiday_calendar" in data:
            calendar_name = data["holiday_calendar"]
            if calendar_name in globals():
                self.holiday_calendar = globals()[calendar_name]()

    def is_trading_day(
        self,
        date
    ) -> bool:
        """
        Is the given date a trading day for the exchange
        """
        return date.weekday() in self.trading_days and not self.is_holiday(date)

    def is_holiday(
        self,
        date
    ) -> bool:
        """
        Check if the given date is a holiday for the exchange

        Using the holidays from the JSON file and the pandas HolidayCalendar if specified

        Args:
                date ([type]): [description]

        Returns:
                [type]: [description]
        """
        is_json_holiday = date.date() in self.holidays
        is_calendar_holiday = (
            self.holiday_calendar
            and date in self.holiday_calendar.holidays(start=date, end=date)
        )
        return is_json_holiday or is_calendar_holiday

    def get_trading_hours(
        self,
        date
    ) -> Tuple[time, time]:
        """
        Get the trading hours for the given date
        """
        for special_day in self.special_trading_days:
            if date.date() == datetime.strptime(special_day["date"], "%Y-%m-%d").date():
                return (
                    datetime.strptime(special_day["open_time"], "%H:%M").time(),
                    datetime.strptime(special_day["close_time"], "%H:%M").time(),
                )
        return self.open_time, self.close_time


# AdvancedTradingCalendar class ----------------------------------------------------------
class TradingCalendar:
    """
    Class for managing trading hours, holidays, and timezones for multiple exchanges

    Example Usage:
            nyse_info = ExchangeInfo('./exchange_calendars/NYSE.json')
            start_date = pd.Timestamp('2023-01-01')
            end_date = pd.Timestamp('2023-01-31')

            nyse_calendar = TradingCalendar(nyse_info, start_date, end_date)

            # Check if a specific time is a trading time
            test_time = pd.Timestamp('2023-01-02 10:00:00', tz='America/New_York')
            print(nyse_calendar.is_trading_time(test_time))

            # Get the next trading time after a given timestamp
            next_time = nyse_calendar.get_next_trading_time(test_time)
            print(next_time)

            # Get trading times between two timestamps
            test_start = pd.Timestamp('2023-01-02', tz='America/New_York')
            test_end = pd.Timestamp('2023-01-03', tz='America/New_York')
            trading_times = nyse_calendar.get_trading_times(test_start, test_end)
            print(trading_times)

            # Get the exchange trading hours
            trading_hours = nyse_calendar.get_exchange_trading_hours()
            print(trading_hours)

            # Reset the calendar with new start and end dates
            nyse_calendar.reset(start_date=pd.Timestamp('2023-02-01'), end_date=pd.Timestamp('2023-02-28'))

            # Step through the calendar
            while not nyse_calendar.is_finished():
                    current_time = nyse_calendar.get_current_time()
                    print(current_time)
                    nyse_calendar.step()
    """

    def __init__(
        self,
        exchange: ExchangeInfo,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
        base_frequency: str = "1D",
    ):  # '1D' for 1 day
        """
        Attributes:
                exchange (ExchangeInfo): The exchange to create the calendar for
                start_date (pd.Timestamp): The start date of the calendar
                end_date (pd.Timestamp): The end date of the calendar
                base_frequency (str): The base frequency of the calendar (e.g. '1D' for 1 day)

        """
        self.exchange = exchange
        self.start_date = start_date
        self.end_date = end_date
        self.base_frequency = base_frequency
        self.calendar = self._create_calendar()
        self.current_step = 0
        self.trade_len = len(self.calendar)

    @error_logger("Error creating calendars")
    def _create_calendar(self) -> Dict[str, pd.DataFrame]:
        """
        Create trading calendars for each exchange.
        We use two methods to create the calendars:
                - The first method uses the holidays and special trading days
                        from the ExchangeInfo object (read JOSN config per exchange)
                - The second method uses the pandas HolidayCalendar for holidays

        Examples:
                - NYSE: USFederalHolidayCalendar()
                - LSE: GoodFriday

        Returns:
                Dict[str, pd.DataFrame]: Dictionary of exchange names and trading calendars

        """
        all_minutes = pd.date_range(
            start=self.start_date,
            end=self.end_date,
            freq="1h",
            tz=self.exchange.timezone,
        )
        calendar = pd.DataFrame(index=all_minutes)

        calendar["is_trading_time"] = calendar.index.map(
            lambda x: (
                self.exchange.is_trading_day(x)
                and self.exchange.open_time <= x.time() < self.exchange.close_time
            )
        )

        # Check for special trading days
        for idx, row in calendar.iterrows():
            if row["is_trading_time"]:
                open_time, close_time = self.exchange.get_trading_hours(idx)
                calendar.at[idx, "is_trading_time"] = (idx.time() >= open_time) and (
                    idx.time() < close_time
                )

        return calendar

    def is_trading_time(
        self,
        timestamp: pd.Timestamp
    ) -> bool:
        """
        Check if the given timestamp is a trading time for the given exchange

        Args:
                timestamp (pd.Timestamp): The timestamp to check

        Returns:
                bool: True if the timestamp is a trading time, False
        """
        return self.calendar.loc[timestamp, "is_trading_time"]

    def step(self):
        if self.is_finished():
            raise RuntimeError(
                "The calendar is finished, please reset it if you want to call it!"
            )
        self.current_step += 1

    def get_current_time(self) -> pd.Timestamp:
        return self.calendar.index[self.current_step]

    def is_finished(self) -> bool:
        return self.current_step >= self.trade_len

    @error_logger("Error resetting calendar")
    def reset(
        self,
        start_date: Optional[pd.Timestamp] = None,
        end_date: Optional[pd.Timestamp] = None,
    ):
        """
        Reset the calendar with new start and end dates

        Args:
                start_date (pd.Timestamp): The new start date
                end_date (pd.Timestamp): The new end date
        """
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
        if start_date or end_date:
            self.calendar = self._create_calendar()
            self.trade_len = len(self.calendar)
        self.current_step = 0

    @error_logger("Error getting next trading time")
    def get_next_trading_time(
        self,
        timestamp: pd.Timestamp
    ) -> pd.Timestamp:
        """
        Get the next trading time after the given timestamp

        Args:
                timestamp (pd.Timestamp): The timestamp to start from

        Returns:
                pd.Timestamp: The next trading time
        """
        future_calendar = self.calendar.loc[timestamp:]
        return future_calendar[future_calendar["is_trading_time"]].index[0]

    @error_logger("Error getting trading times")
    def get_trading_times(
        self,
        start: pd.Timestamp,
        end: pd.Timestamp
    ) -> pd.DatetimeIndex:
        return self.calendar.loc[start:end][self.calendar["is_trading_time"]].index

    def get_exchange_trading_hours(self) -> Tuple[time, time]:
        return self.exchange.open_time, self.exchange.close_time

    def get_exchange_timezone(self) -> timezone:
        return self.exchange.timezone

    def __repr__(self) -> str:
        return (
            f"TradingCalendar({self.exchange.name}, {self.start_date}~{self.end_date}, "
            f"Step: [{self.current_step}/{self.trade_len}])"
        )


# UnitTests Class --------------------------------------------------------------
class UnitTests(Enum):
    CREATE_CALENDAR = 1
    IS_TRADING_TIME = 2
    GET_NEXT_TRADING_TIME = 3
    GET_TRADING_TIMES = 4
    GET_EXCHANGE_TRADING_HOURS = 5


async def run_unit_test(unit_test: UnitTests):

    nyse_info = ExchangeInfo("./quantjourney/calendars/exchange_calendars/NYSE.json")
    start_date = pd.Timestamp("2023-01-05")
    end_date = pd.Timestamp("2023-01-31")

    nyse_calendar = TradingCalendar(nyse_info, start_date, end_date)

    if unit_test == UnitTests.CREATE_CALENDAR:
        print("Calendar created:")
        print(nyse_calendar.calendar.head(20))
        print(nyse_calendar.calendar.tail(20))

    elif unit_test == UnitTests.IS_TRADING_TIME:
        test_time = pd.Timestamp("2023-01-05 10:00:00", tz="America/New_York")
        print(f"Is trading time for NYSE at {test_time}:")
        print(nyse_calendar.is_trading_time(test_time))

    elif unit_test == UnitTests.GET_NEXT_TRADING_TIME:
        test_time = pd.Timestamp("2023-01-02 16:01:00", tz="America/New_York")
        next_time = nyse_calendar.get_next_trading_time(test_time)
        print(f"Next trading time after {test_time}:")
        print(next_time)

    elif unit_test == UnitTests.GET_TRADING_TIMES:
        test_start = pd.Timestamp("2023-01-05", tz="America/New_York")
        test_end = pd.Timestamp("2023-01-06", tz="America/New_York")
        trading_times = nyse_calendar.get_trading_times(test_start, test_end)
        print(f"Trading times between {test_start} and {test_end}:")
        print(trading_times)

    elif unit_test == UnitTests.GET_EXCHANGE_TRADING_HOURS:
        trading_hours = nyse_calendar.get_exchange_trading_hours()
        print("NYSE trading hours:")
        print(trading_hours)

    else:
        raise ValueError(f"Unknown unit test: {unit_test}")


async def main():

    unit_test = UnitTests.CREATE_CALENDAR
    is_run_all_tests = True
    if is_run_all_tests:
        for unit_test in UnitTests:
            print(f"\n--- Running unit test: {unit_test.name} ---")
            await run_unit_test(unit_test)
    else:
        print(f"\n--- Running unit test: {unit_test.name} ---")
        await run_unit_test(unit_test=unit_test)


if __name__ == "__main__":
    asyncio.run(main())
