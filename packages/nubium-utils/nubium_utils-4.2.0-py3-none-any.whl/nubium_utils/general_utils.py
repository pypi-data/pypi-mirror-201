from datetime import datetime
from typing import Union
from os import remove
from dateutil import parser
from dateutil.parser import ParserError
from pytz import timezone


def universal_datetime_converter(incoming_datetime: Union[str, datetime], incoming_timezone: timezone = timezone("Etc/UTC")) -> str:
    """
    Converts datetime values of all kinds into a normalized format
    Assumes midnight if datetime does not include time
    """
    universal_format = '%Y-%m-%dT%H:%M:%SZ'

    try:
        datetime_to_convert = parser.parse(str(incoming_datetime))
    except (ParserError, OverflowError):
        try:
            return datetime.utcfromtimestamp(int(incoming_datetime)).strftime(universal_format)
        except Exception:
            return ""

    if datetime_to_convert.tzinfo is None or datetime_to_convert.tzinfo.utcoffset(datetime_to_convert) is None:
        datetime_to_convert = incoming_timezone.normalize(incoming_timezone.localize(datetime_to_convert))

    datetime_to_convert = datetime_to_convert.astimezone(timezone("Etc/UTC"))
    converted_datetime = datetime_to_convert.strftime(universal_format)
    return converted_datetime


def del_kubernetes_healthcheck_file(health_path='/tmp'):
    try:
        remove(f'{health_path}/health')
    except:
        pass


def write_kubernetes_healthcheck_file(health_path='/tmp'):
    del_kubernetes_healthcheck_file(health_path=health_path)
    with open(f'{health_path}/health', 'w') as health_file:
        health_file.write('Healthy')
