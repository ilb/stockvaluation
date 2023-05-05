import pandas as pd

from datetime import date, timedelta


class DateUtils:

    def date_range(self, date_str, delta=-30):
        """Gets the end date and delta, returns date range list."""
        date_end = self._get_iso_format(date_str)
        date_start = date_end + timedelta(days=delta)
        return pd.date_range(str(date_start), str(date_end))

    def get_end_date(self, date_str):
        date_end = date.fromisoformat(date_str)
        if date_end == date.today():
            date_end = date_end + timedelta(days=-1)
        return str(date_end)

    def _get_iso_format(self, date_str):
        return date.fromisoformat(date_str)
