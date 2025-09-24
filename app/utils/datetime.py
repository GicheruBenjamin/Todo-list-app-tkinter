# app/utils/datetime.py
"""
Datetime utils.
class Datetime:
    @staticmethod
    from_cast(cast : str, fmt : str = "%d/%m/%Y") -> datetime:
        get datetime from cast i.e dd/mm/yyyy
        ~cast : str
        ~return : datetime
    @staticmethod
    to_cast(dt : datetime, fmt : str = "%d/%m/%Y") -> str:
        get cast from datetime i.e dd/mm/yyyy
        ~datetime : datetime
        ~return : str
    @staticmethod
    today(fmt : str = "%d/%m/%Y") -> str:
        get today's date as a string in the given format
        ~return : str

"""

# app/utils/datetime.py
"""
Datetime utilities.
Provides safe conversion between datetime objects and string casts.
"""

from datetime import datetime

class DateUtils:
    @staticmethod
    def from_cast(cast: str, fmt: str = "%d/%m/%Y") -> datetime:
        """
        Convert a string (cast) to a datetime object.
        Default format: dd/mm/yyyy
        """
        try:
            return datetime.strptime(cast, fmt)
        except ValueError:
            raise ValueError(f"Invalid date format: '{cast}'. Expected format: {fmt}")

    @staticmethod
    def to_cast(dt: datetime, fmt: str = "%d/%m/%Y") -> str:
        """
        Convert a datetime object to a string (cast).
        Default format: dd/mm/yyyy
        """
        return dt.strftime(fmt)

    @staticmethod
    def today(fmt: str = "%d/%m/%Y") -> str:
        """
        Get today's date as a string in the given format.
        """
        return datetime.today().strftime(fmt)
