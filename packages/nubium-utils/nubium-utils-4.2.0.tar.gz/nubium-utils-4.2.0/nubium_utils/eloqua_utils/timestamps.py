from datetime import datetime
from typing import Literal
from nubium_utils.general_utils import universal_datetime_converter

import pytz

TimestampForm = Literal["%Y-%m-%dT%H:%M:%SZ"]

# timestamps/nst = str rep; dt = datetime obj


def _timestamp_to_dt(timestamp_in: str, ts_form: str) -> datetime:
    return datetime.strptime(timestamp_in, ts_form)


def _dt_set_utc(datetime_obj: datetime) -> datetime:
    return pytz.utc.localize(datetime_obj)


def _dt_utc_to_eastern(utc_datetime_obj: datetime) -> datetime:
    return utc_datetime_obj.astimezone(tz=pytz.timezone("US/Eastern"))


def _dt_to_timestamp(datetime_obj: datetime, ts_form: str) -> str:
    return datetime_obj.strftime(ts_form)


def eloqua_epoch_to_nst(epoch) -> str:
    """
    Eloqua modified/updated at timestamps should return as epochs, which can then be converted to NST via this.
    """
    return universal_datetime_converter(str(epoch))


def nst_to_eloqua_query_timestamp(nst: str) -> str:
    """ Format for v1.0 API search queries in eloqua (uses Eastern)"""
    return _dt_to_timestamp(_dt_utc_to_eastern(_dt_set_utc(_timestamp_to_dt(nst, "%Y-%m-%dT%H:%M:%SZ"))), "%Y-%m-%d %H:%M:%S")
