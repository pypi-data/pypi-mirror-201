from datetime import date
from functools import cached_property, cache
from typing import Optional

from algora.common.date.calendar.market_calendar import MarketCalendar
from algora.quant.model.enum import BusinessDayConvention
from algora.quant.model.period import Period


class Schedule:
    def __init__(
        self,
        start_date: date,
        end_date: date,
        calendar: MarketCalendar,
        period: Period,
        convention: BusinessDayConvention,
    ):
        self._start_date: date = start_date
        self._end_date: date = end_date

        self._calendar: MarketCalendar = calendar
        self._period: Period = period
        self._convention: BusinessDayConvention = convention

        self._last: Optional[date] = None
        self._current: date = self._start_date

    @cached_property
    def start_date(self):
        """
        The adjusted start date.

        NOTE: This date is adjusted using the passed in convention
        """
        return self._get_valid_day(self._start_date)

    @cached_property
    def end_date(self):
        """
        The adjusted end date.

        NOTE: This date is adjusted using the passed in convention
        """
        return self._get_valid_day(self._end_date)

    @property
    def current(self):
        """
        The adjusted current date.

        NOTE: This date is adjusted using the passed in convention
        """
        return self._get_valid_day(self._current)

    def _value(self):
        """ """
        if self.current < self.start_date:
            return self.start_date
        elif self.current > self.end_date:
            return self.end_date
        return self.current

    @cache
    def _get_valid_day(self, as_of_date: date):
        """
        Gets the closest valid day to the as_of_date passed in

        NOTE: This date is adjusted using the passed in convention

        Parameters:
            as_of_date (date): Date being validated/adjusted

        Returns:
            date: The as_of_date if valid otherwise it is the adjusted date
        """
        if self._calendar.is_business_day(as_of_date):
            return as_of_date
        else:
            return self._calendar.adjust(as_of_date, self._convention)

    def _step(self):
        """
        One step in the iteration process

        Returns
            (date): The date for the step
        """
        result = self._value()
        if result == self.end_date:
            self._last = self.end_date

        while result == self.current:
            advanced_date = self._period.advance(self._current)
            self._last = self.current
            self._current = advanced_date

        return result

    def __iter__(self):
        return self

    def __next__(self):
        # Stop if we have met or exceeded the end_date
        if self._last and self._last >= self.end_date:
            raise StopIteration

        # Get the next value in the iteration, and take the required number of steps to update for next set of iteration
        return self._step()
