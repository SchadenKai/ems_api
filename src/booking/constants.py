from enum import Enum
from datetime import datetime

class TimeSchedule(Enum):
    EIGHT_AM = "EIGHT_AM"
    NINE_AM = "NINE_AM"
    TEN_AM = "TEN_AM"
    ELEVEN_AM = "ELEVEN_AM"
    TWELVE_PM = "TWELVE_PM"
    ONE_PM = "ONE_PM"
    TWO_PM = "TWO_PM"
    THREE_PM = "THREE_PM"
    FOUR_PM = "FOUR_PM"

TimeScheduleObject = {
    "EIGHT_AM": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 8, 0),
    "NINE_AM": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 9, 0),
    "TEN_AM": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 10, 0),
    "ELEVEN_AM": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 11, 0),
    "TWELVE_PM": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 12, 0),
"ONE_PM": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 13, 0),
    "TWO_PM": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 14, 0),
    "THREE_PM": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 15, 0),
    "FOUR_PM": datetime(datetime.now().year, datetime.now().month, datetime.now().day, 16, 0)
}

class BookingRange(Enum):
    TODAY = "today"
    WEEK = "week"
    MONTH = "month"