import math
import os
import random
import re
import string
from datetime import datetime, timedelta
import nanoid
import uuid

import pytz
from django.conf import settings

from common.constant.constant import RegexPattern
from common.constant.date_time import FormatDateTime
from common.custom.exceptions import APIError


def check_regex(pattern, input_string):
    return re.match(pattern, input_string)


def get_current_time(time_zone=settings.TIME_ZONE):
    current_time = datetime.now().astimezone(tz=pytz.timezone(time_zone))
    return current_time


def get_current_time_plus_one_min(time_zone=settings.TIME_ZONE):
    current_time = datetime.now().astimezone(tz=pytz.timezone(time_zone))
    return current_time + timedelta(minutes=1)


def get_str_time_now(str_format="%Y-%m-%d_%H-%M-%S", time_zone=settings.TIME_ZONE):
    current_time = get_current_time(time_zone)
    return current_time.strftime(str_format)


def get_str_time_now_for_csv(str_format="%Y%m%d%H%M%S", time_zone=settings.TIME_ZONE):
    current_time = get_current_time(time_zone)
    return current_time.strftime(str_format)


def get_upload_to(instance, filename):
    return os.path.join(instance.UPLOAD_TO, str(instance.pk), filename.split("/")[-1])


# def get_upload_to(instance, filename):
#     generate_filename = f"{generate_uuid(16)}_{filename.split('/')[-1]}"
#     return os.path.join(instance.UPLOAD_TO, generate_filename)


def get_source_field_model(name_model, *args):
    return ".".join((name_model, *args))


def str2bool(content):
    return str(content).lower() in ("yes", "true", "t", "1")


def generate_password(length_min: int = 7, length_max: int = 15):
    """
    Generate password with input length.
    Password include lowercase, uppercase, digit.

    Args:
        length_min (int): mix length password, default is 7
        length_max (int): max length password, default is 15

    Returns:
        Password value
    """
    password_length = random.randint(length_min, length_max)
    random_source = string.ascii_letters + string.digits
    password = "".join(random.choice(random_source) for _ in range(password_length))
    return password


def to_snake_case(data) -> str:
    """Convert an input string in CamelCase to snake_case.
    Args:
        data (str): input string
    Returns:
        snake_case string (str)
    """
    return re.sub(r"" + RegexPattern.SNAKE_CASE.value, "_", data).lower()


# Round value base on math logic
# Example:
# - 1.1 => 1
# - 1.5 => 2
# - 1.9 => 2
def round_half_up(n):
    return int(math.floor(float(n) + 0.5) / 1)


# Format digit value to currency format with comma every 3 integers
# Example:
# - 10000.2345 => 10,000.2345
def currency_format(n):
    return "{:,}".format(n)


# Convert datetime object to JST timezone
# Replace string format
def convert_datetime_to_jst_str(date, jst_format):
    replace_tz = date.astimezone(pytz.timezone(settings.TIME_ZONE))
    return replace_tz.strftime(jst_format)


# Convert datetime object to JST timezone
# Return date object
def convert_any_datetime_to_jst_date(dt: datetime) -> datetime.date:
    if not tz_aware(dt):
        raise APIError(
            "Cant convert datetime without timezone attribute to JST timezone"
        )
    replace_tz = dt.astimezone(pytz.timezone(settings.TIME_ZONE))
    return replace_tz.date()


# Check datetime object localized with timezone
def tz_aware(dt: datetime) -> bool:
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


def convert_str_to_date(date_str, format=FormatDateTime.DATE_YMD.value):
    """
    Todo: Convert date string to date with specific date format.
    """
    try:
        return datetime.strptime(date_str, format)
    except Exception:
        return None


def convert_str_to_date_only(date_str, format=FormatDateTime.DATE_YMD.value):
    """
    Todo: Convert date string to date with specific date format.
    """
    try:
        return datetime.strptime(date_str, format).date()
    except Exception:
        return None


def generate_uuid(
    length: int = 10,
    chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
):
    uuid = nanoid.generate(chars, size=length)
    return uuid


def generate_otp(
    length: int = 6,
    chars: str = "0123456789",
):
    otp = nanoid.generate(chars, size=length)
    return otp


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
