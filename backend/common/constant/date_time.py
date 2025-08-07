from enum import Enum


class DateTimeFields(str, Enum):
    YEAR = "%Y"
    MONTH = "%m"
    DAY = "%d"
    DATETIME = "%m/%d/%Y, %H:%M:%S"
    SEPARATOR = " "


class FormatDateTime(str, Enum):
    DATE_TIME_YMD_HM_JP: str = "%Y年%m月%d日%H:%M"
    DATE_TIME_YMD_HMS_FZ_JP: str = "%Y-%m-%d %H:%M:%S.%f%z"
    DATE_TIME_YMD = "%Y/%m/%d/"
    DATETIME_CSV = "%Y%m%d"
    DATE_TIME_YMD_HMS = "%Y-%m-%d %H:%M:%S"
    DATE_YMD_JP: str = "%Y年%m月%d日"
    DATE_YMD_OF_DAY_HM_JP: str = "%Y年%m月%d日(曜日)%H:%M"
    DATE_YMD_HM_JP: str = "%Y年%m月%d日(曜日)%H時%M分"
    DATE_MD_OF_WEEK_JP: str = "%m月%d日(曜日)"
    DATE_MD_H_JP: str = "%m月%d日%H時"  # Month-Day-Hour
    # Month-Day-Day_of_Week-Hour-Minute
    DATE_MD_DOW_HM_JP: str = "%m月%d日(%A)%H時%M分"
    DATE_YMD_DOW_HM_JP: str = (
        "%Y年%m月%d日(%A)%H:%M"  # Year-Month-Day-Day_of_Week-Hour-Minute
    )
    DATE_MD_DOW_JP: str = "%m月%d日(%A)"  # Month-Day-Day_of_Week
    DATE_HM_JP: str = "%H時%M分"
    COMMENT_DATETIME = "%Y/%m/%d"
    DATE_YMD: str = "%Y-%m-%d"
