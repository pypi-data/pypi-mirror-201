from calendar import Calendar
import datetime

from canada_holiday.utils import (
    DAY_TO_INDEX,
    find_easter_day,
    get_last_day_str_of_month,
    parse_preceding_day_str,
)

cal = Calendar()


class CanadaHoliday:
    def __init__(
        self,
        name: str,
        month: int,
        year: int = None,
        day: int = None,
        day_of_the_week: str = None,
        date: datetime.date = None,
        nearest_day: (str, int) = None,
        nth_day: (str, int) = None,
        preceding_date: (str, int) = None,
        province: str = None,
        succeeding_date: (str, int) = None,
    ):
        self.name = name
        self.month = month
        self.year = year
        self.day = day
        self._day_of_the_week = day_of_the_week
        self._date = date  # ex: datetime.date(2023, 12, 25)
        self.nearest_day = nearest_day
        self.nth_day = nth_day
        self.preceding_date = preceding_date
        self.province = province
        self.succeeding_date = succeeding_date

    def __repr__(self):
        return f"CanadaHoliday({self.name}, {self.date}, {self.day_of_the_week}, {self.province})"

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date: datetime.date):
        self._date = date

    @property
    def day_of_the_week(self):
        return self._day_of_the_week

    @day_of_the_week.setter
    def day_of_the_week(self, day_of_the_week: str):
        self._day_of_the_week = day_of_the_week

    def get_nth_day_holiday(self, year: int) -> datetime.date:
        if self.preceding_date or self.succeeding_date or self.nearest_day:
            raise Exception(f"Please check the Holiday: {self.name}.")
        day_of_the_week, n = self.nth_day
        day_of_the_week_idx = DAY_TO_INDEX[day_of_the_week]
        day_in_first_week = cal.monthdatescalendar(year, self.month)[0][
            day_of_the_week_idx
        ]
        if day_in_first_week.month == self.month:
            return cal.monthdatescalendar(year, self.month)[n - 1][day_of_the_week_idx]
        else:
            return cal.monthdatescalendar(year, self.month)[n][day_of_the_week_idx]

    def get_preceding_day_holiday(self, year: int) -> datetime.date:
        if self.nth_day or self.succeeding_date or self.nearest_day:
            raise Exception(f"Please check the Holiday: {self.name}.")

        (
            day_of_the_week,
            preceding_day,
        ) = self.preceding_date  # ex: Monday before May 25th
        day_of_the_week_idx = DAY_TO_INDEX[day_of_the_week]

        if isinstance(preceding_day, str):
            pre_day_str1, pre_day_str2 = parse_preceding_day_str(preceding_day)
            if pre_day_str1.lower() == "last":
                precede_date = get_last_day_str_of_month(
                    year, self.month, pre_day_str2.lower()
                )
            elif preceding_day == "Easter Sunday":
                precede_date = find_easter_day(year)
        else:
            precede_date = datetime.date(year, self.month, preceding_day)
        precede_day_idx = precede_date.weekday()
        delta_days = abs(precede_day_idx - day_of_the_week_idx)
        # Find 'day_str' before easter_day
        return precede_date - datetime.timedelta(days=delta_days)

    def get_succeeding_day_holiday(self, year: int) -> datetime.date:
        if self.nth_day or self.preceding_date or self.nearest_day:
            raise Exception(f"Please check the Holiday: {self.name}.")

        (
            day_of_the_week,
            succeeding_day,
        ) = self.succeeding_date  # ex: Monday after Easter Sunday
        day_of_the_week_idx = DAY_TO_INDEX[day_of_the_week]

        if succeeding_day == "Easter Sunday":
            succeed_date = find_easter_day(year)
        else:
            succeed_date = datetime.date(year, self.month, succeeding_day)
        succeed_day_idx = succeed_date.weekday()
        delta_days = abs(succeed_day_idx - day_of_the_week_idx)
        return succeed_date + datetime.timedelta(days=(7 - delta_days))

    def get_nearest_day_holiday(self, year: int) -> datetime.date:
        """
        Example of calculating a nearest Monday:
        - if holiday day is 23:
            - if 23 is Sunday (6)    Monday (0) day + (7 - delta:6)
            - if 23 is Tuesday (1)   Monday (0) day - delta:1
            - if 23 is Wednesday (2) Monday (0) day - delta:2
            - if 23 is Thursday (3)  Monday (0) day - delta:3
            - if 23 is Friday (4)    Monday (0) day + (7 - delta:4)
            - if 23 is Saturday (5)  Monday (0) day + (7 - delta:5)
        """
        if self.nth_day or self.preceding_date or self.succeeding_date:
            raise Exception(f"Please check the Holiday: {self.name}.")

        day_str, nearest_day = self.nearest_day
        day_str_idx = DAY_TO_INDEX[day_str]
        nearest_date = datetime.date(year, self.month, self.nearest_day[1])
        nearest_day_str_idx = nearest_date.weekday()
        delta_days = abs(day_str_idx - nearest_day_str_idx)

        if delta_days < 4:
            return nearest_date - datetime.timedelta(delta_days)
        else:
            return nearest_date + datetime.timedelta(7 - delta_days)

    def to_date(self, year: int):
        """
        Calculate the datetime.date of the given holiday
        """
        if (
            not self.nth_day
            and not self.preceding_date
            and not self.succeeding_date
            and not self.nearest_day
        ):
            return datetime.date(year, self.month, self.day)

        date = None
        if self.nth_day:
            date = self.get_nth_day_holiday(year)
        elif self.preceding_date:
            date = self.get_preceding_day_holiday(year)
        elif self.succeeding_date:
            date = self.get_succeeding_day_holiday(year)
        elif self.nearest_day:
            date = self.get_nearest_day_holiday(year)

        return date
