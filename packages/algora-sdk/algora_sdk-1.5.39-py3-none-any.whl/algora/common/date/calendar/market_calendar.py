import calendar
import datetime
from typing import Optional, List

import pandas as pd
from datetime import date
from pandas_market_calendars import get_calendar, MarketCalendar as PandasMarketCalendar

from algora.quant.model.enum import BusinessDayConvention


class MarketCalendar:
    def __init__(self, name: str):
        self._calendar: PandasMarketCalendar = get_calendar(name)

    @property
    def calendar(self) -> PandasMarketCalendar:
        """
        This is a property exposing the wrapped pandas_market_calendar.MarketCalendar object.
        """
        return self._calendar

    def window(
        self,
        start_date: date,
        end_date: date,
        tz: str = "UTC",
        start: str = "market_open",
        end: str = "market_close",
        force_special_times: bool = True,
        market_times: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        This exposes the schedule method from the wrapped pandas_market_calendar.MarketCalendar object.

        Parameters:
            start_date (date): Start date for the schedule period
            end_date (date): End date for the schedule period
            tz (str): Timezone that the columns of the returned schedule are in, default: "UTC"
            start (str): The first market_time to include as a column, default: "market_open"
            end (str): The last market_time to include as a column, default: "market_close"
            force_special_times (bool): How to handle special times.
                True: Overwrite regular times of the column itself, conform other columns to special times of
                    market_open/market_close if those are requested.
                False: Only overwrite regular times of the column itself, leave others alone
                None: Completely ignore special times
            market_times (Optional[List[str]]): Alternative to start/end, list of market_times that are in
                self.regular_market_times
        Returns:
            pd.Dataframe: A dataframe indexed by dates containing two columns of market_open and market_close. The
            returned dataframe contains all the valid businesses days between the start_date and end_date.
        """
        return self.calendar.schedule(
            start_date, end_date, tz, start, end, force_special_times, market_times
        )

    def is_business_day(self, as_of_date: date) -> bool:
        """
        Check if the passed in date is a business day.

        Parameters:
            as_of_date (date): The date that is checked to see if it is a business day

        Returns:
            bool: A flag representing if the as_of_date is a business day
        """
        window = self.window(start_date=as_of_date, end_date=as_of_date)
        return not window.empty

    def is_holiday(self, as_of_date: date) -> bool:
        """
        Check if the passed in date is a holiday.

        NOTE: This returns false for holidays that occur during the weekends
        NOTE: This is not stable for adhoc_holiday and holidays that change dates each year

        Parameters:
            as_of_date (date): The date that is checked to see if it is a holiday

        Returns:
            bool: A flag representing if the as_of_date is a holiday
        """
        is_general_holiday = False
        is_adhoc_holiday = as_of_date in [
            ts.date() for ts in self.calendar.adhoc_holidays
        ]
        if self.calendar.regular_holidays:
            is_general_holiday = any(
                self.calendar.regular_holidays.holidays().isin([as_of_date])
            )
        return is_adhoc_holiday or is_general_holiday

    def is_weekend(self, as_of_date: date) -> bool:
        """
        Check if the passed in date is a weekend.

        Parameters:
            as_of_date (date): The date that is checked to see if it is a weekend

        Returns:
            bool: A flag representing if the as_of_date is a weekend
        """
        weekdays = self.calendar.weekmask.split(" ")
        day_of_week = calendar.day_name[as_of_date.weekday()][:3]
        is_weekend = day_of_week not in weekdays
        special_cases = not self.is_holiday(as_of_date) and not self.is_business_day(
            as_of_date
        )
        return is_weekend or special_cases

    def is_end_of_month(self, as_of_date: date) -> bool:
        """
        Check if the passed in date is the last day of the month.

        Parameters:
            as_of_date (date): The date that is checked to see if it is the last day of the month

        Returns:
            bool: A flag representing if the as_of_date is the last day of the month
        """
        return as_of_date == self.end_of_month(as_of_date)

    def end_of_month(self, as_of_date: date) -> date:
        """
        Gets the last day of the month for the month of the day passed in.

        Parameters:
            as_of_date (date): The date used to get the month

        Returns:
            date: The last day of the month of the date passed in
        """
        _, days_in_month = calendar.monthrange(as_of_date.year, as_of_date.month)
        first_day = date(as_of_date.year, as_of_date.month, 1)
        last_day = date(as_of_date.year, as_of_date.month, days_in_month)
        df = self.window(first_day, last_day)
        return df.index[-1].date()

    def adjust(self, as_of_date: date, convention: BusinessDayConvention) -> date:
        """
        This method adjusts the date passed in. The types of adjustments are outlined below.

        Business day convention
            FOLLOWING: The date is corrected to the first working day that follows.

            MODIFIED_FOLLOWING: The date is corrected to the first working day after that, unless this working day is in
             the next month; if the modified working day is in the next month, the date is corrected to the last working
             day that appears before, to ensure the original The date and the revised date are in the same month.

            PRECEDING: Correct the date to the last business day that Preceding before.

            MODIFIED_PRECEDING: Modify the date to the last working day that appeared before, unless the working sunrise
             is now the previous month; if the modified working sunrise is now the previous month, the date is modified
             to the first working day after that The original date and the revised date are guaranteed to be in the same
             month.

            UNADJUSTED: No adjustment.

        Parameters:
            as_of_date (date): The date being corrected
            convention (BusinessDayConvention): Business day convention

        Returns:
            date: The adjusted date
        """
        if convention == convention.UNADJUSTED:
            return as_of_date
        elif convention == convention.FOLLOWING:
            return self._following(as_of_date)
        elif convention == convention.MODIFIED_FOLLOWING:
            return self._modified_following(as_of_date)
        elif convention == convention.PRECEDING:
            return self._preceding(as_of_date)
        elif convention == convention.MODIFIED_PRECEDING:
            return self._modified_preceding(as_of_date)
        else:
            raise Exception(f"BusinessDayConvention '{convention}' not supported")

    def _following(self, as_of_date: date) -> date:
        """
        Gets the next working day.

        Parameters:
            as_of_date (date): The date being adjusted

        Returns:
            date: The next working day
        """
        start = as_of_date + datetime.timedelta(days=1)
        end = as_of_date + datetime.timedelta(days=8)
        window = self.window(start_date=start, end_date=end)
        return window.index[0].date()

    def _modified_following(self, as_of_date: date) -> date:
        """
        Gets the first working day after the passed in date, unless the next working day is in the next month;
        if it is it gets the last working day that appears before the passed in date.

        Parameters:
            as_of_date (date): The date being adjusted

        Returns:
            date: The next 'modified' working day
        """
        following = self._following(as_of_date)
        if following.month == as_of_date.month:
            return following

        return self._preceding(as_of_date)

    def _preceding(self, as_of_date: date) -> date:
        """
        Gets the previous working day.

        Parameters:
            as_of_date (date): The date being adjusted

        Returns:
            date: The previous working day
        """
        start = as_of_date - datetime.timedelta(days=8)
        end = as_of_date - datetime.timedelta(days=1)
        window = self.window(start_date=start, end_date=end)
        return window.index[-1].date()

    def _modified_preceding(self, as_of_date: date) -> date:
        """
        Gets the last working day that appeared before the passed in date, unless it is in the previous month; if the
        modified it is it gets the first working day after that the date passed in.

        Parameters:
            as_of_date (date): The date being adjusted

        Returns:
            date: The previous 'modified' working day
        """
        preceding = self._preceding(as_of_date)
        if preceding.month == as_of_date.month:
            return preceding

        return self._following(as_of_date)
