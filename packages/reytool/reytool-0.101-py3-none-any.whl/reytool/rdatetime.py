# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:11:50
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's time methods.
"""


from typing import Any, Tuple, Dict, Literal, Optional, Union, overload
import time
import datetime
from pandas import DataFrame, concat as pd_concat

from .rbasic import check_target, is_number_str
from .rregular import re_search
from .rtext import rprint


@overload
def now(
    format: Literal["datetime", "date", "time", "timestamp", "datetime_str", "date_str", "time_str"] = "datetime_str"
) -> Union[datetime.datetime, datetime.date, datetime.time, int, str]: ...

@overload
def now(format: Literal["datatime"]) -> datetime.datetime: ...

@overload
def now(format: Literal["date"]) -> datetime.date: ...

@overload
def now(format: Literal["time"]) -> datetime.time: ...

@overload
def now(format: Literal["datetime_str", "date_str", "time_str"]) -> str: ...

@overload
def now(format: Literal["timestamp"]) -> int: ...

def now(
    format: Literal["datetime", "date", "time", "datetime_str", "date_str", "time_str", "timestamp"] = "datetime_str"
) -> Union[datetime.datetime, datetime.date, datetime.time, str, int]:
    """
    Get current time string or intger or object.

    Parameters
    ----------
    format : Format type.
        - Literal['datetime'] : Return datetime object of datetime package.
        - Literal['date'] : Return date object of datetime package.
        - Literal['time'] : Return time object of datetime package.
        - Literal['datetime_str'] : Return string in format '%Y-%m-%d %H:%M:%S'.
        - Literal['date_str'] : Return string in format '%Y-%m-%d'.
        - Literal['time_str'] : Return string in foramt '%H:%M:%S'.
        - Literal['timestamp'] : Return timestamp in milliseconds.

    Returns
    -------
    Time string or object of datetime package.
    """

    # Return time object by parameter format.
    if format == "datetime":
        return datetime.datetime.now()
    elif format == "date":
        return datetime.datetime.now().date()
    elif format == "time":
        return datetime.datetime.now().time()
    elif format == "datetime_str":
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif format == "date_str":
        return datetime.datetime.now().strftime("%Y-%m-%d")
    elif format == "time_str":
        return datetime.datetime.now().strftime("%H:%M:%S")
    elif format == "timestamp":
        return int(time.time() * 1000)

@overload
def time_to_str(
    time_obj: Union[datetime.datetime, datetime.date, datetime.time, datetime.timedelta, Any],
    format_str: Optional[str] = None,
    throw_error: bool = False
) -> Union[str, Any]: ...

@overload
def time_to_str(time_obj: Union[datetime.datetime, datetime.date, datetime.time, datetime.timedelta]) -> str: ...

@overload
def time_to_str(time_obj: Any) -> Any: ...

def time_to_str(
    time_obj: Union[datetime.datetime, datetime.date, datetime.time, datetime.timedelta, Any],
    format_str: Optional[str] = None,
    throw_error: bool = False
) -> Union[str, Any]:
    """
    Format time object of datetime package as string

    Parameters
    ----------
    time_obj : Of datetime package.
    format_str : Format string.
        - None : Automatic by type.
            * Parameter 'time_obj' is datetime.datetime : Is '%Y-%m-%d %H:%M:%S'.
            * Parameter 'time_obj' is datetime.date : Is '%Y-%m-%d'.
            * Parameter 'time_obj' is datetime.time : Is '%H:%M:%S'.
            * Parameter 'time_obj' is datetime.timedelta : Is f'{days} %H:%M:%S'.
        - str : Format by str.

    throw_error : Whether throw error, when parameter 'time_obj' value error, otherwise return original value.

    Returns
    -------
    String after foramt or original value.
    """

    # Check parameters.
    if throw_error:
        check_target(time_obj, datetime.datetime, datetime.date, datetime.time, datetime.timedelta)

    # Convert to time string.

    ## From datetime object.
    if type(time_obj) == datetime.datetime:
        if format_str == None:
            string = str(time_obj)[:19]
        else:
            string = time_obj.strftime(format_str)

    ## From date object.
    elif type(time_obj) == datetime.date:
        if format_str == None:
            string = str(time_obj)[:10]
        else:
            string = time_obj.strftime(format_str)

    ## From time object.
    elif type(time_obj) == datetime.time:
        if format_str == None:
            string = str(time_obj)[:8]
        else:
            string = time_obj.strftime(format_str)

    ## From timedelta object.
    elif type(time_obj) == datetime.timedelta:
        if format_str == None:
            string = str(time_obj)
            if "day" in string:
                day, char, string = string.split(" ")
            else:
                day = "0"
            if string[1] == ":":
                string = "0" + string
            string = "%s %s" % (day, string[:8])
        else:
            seconds = time_obj.seconds
            time_obj = time.gmtime(seconds)
            string = time.strftime(format_str, time_obj)

    ## From other object.
    else:
        return time_obj

    return string

@overload
def str_to_time(
    string: Union[str, Any],
    to_type: Optional[Literal["datetime", "date", "time", "timedelta", "timestamp"]] = None,
    format_str: Optional[str] = None,
    throw_error: bool = False
) -> Union[datetime.datetime, datetime.date, datetime.time, datetime.timedelta, int, Any]: ...

@overload
def str_to_time(to_type: Literal["datetime"]) -> Union[datetime.datetime, Any]: ...

@overload
def str_to_time(to_type: Literal["date"]) -> Union[datetime.date, Any]: ...

@overload
def str_to_time(to_type: Literal["time"]) -> Union[datetime.time, Any]: ...

@overload
def str_to_time(to_type: Literal["timedelta"]) -> Union[datetime.timedelta, Any]: ...

@overload
def str_to_time(to_type: Literal["timestamp"]) -> Union[int, Any]: ...

@overload
def str_to_time(to_type: None) -> Union[datetime.datetime, datetime.date, datetime.time, datetime.timedelta, Any]: ...

def str_to_time(
    string: Union[str, Any],
    to_type: Optional[Literal["datetime", "date", "time", "timedelta", "timestamp"]] = None,
    format_str: Optional[str] = None,
    throw_error: bool = False
) -> Union[datetime.datetime, datetime.date, datetime.time, datetime.timedelta, int, Any]:
    """
    Format string as time object of datetime package

    Parameters
    ----------
    string : Time string.
    to_type : Format type.
        - None : Automatic judgment.
        - Literal['datetime'] : Return datetime object of datetime package.
        - Literal['date'] : Return date object of datetime package.
        - Literal['time'] : Return time object of datetime package.
        - Literal['timedelta'] : Return timedelta object of datetime package.
        - Literal['timestamp'] : Return timestamp in milliseconds.

    format_str : Format string.
        - None : Default format method.
            * Parameter 'to_type' is 'datetime' : Is '%Y-%m-%d %H:%M:%S'.
            * Parameter 'to_type' is 'date' : Is '%Y-%m-%d'.
            * Parameter 'to_type' is 'time' : Is '%H:%M:%S'.
            * Parameter 'to_type' is 'timedelta' : Is 'days %H:%M:%S'.
            * Parameter 'to_type' is 'timestamp' : Is '%Y-%m-%d %H:%M:%S'.
            * Parameter 'to_type' is None : automatic judgment.
        - str : Format by str.

    throw_error : Whether throw error, when parameter 'time_obj' value error, otherwise return original value.

    Returns
    -------
    Time object of datetime package or timestamp or original value.
    """

    # Check parameters.
    if type(string) != str:
        return string

    # Get time format by automatic judgment.
    if to_type == None:
        str_len = len(string)
        if "年" == string[4:5]:
            if str_len > 11:
                format_str = "%Y年%m月%d日 %H时%M分%S秒"
                to_type = "datetime"
            else:
                format_str = "%Y年%m月%d日"
                to_type = "date"
        elif "时" in string[1:3]:
            format_str = "%H时%M分%S秒"
            to_type = "time"
        elif " " in string and "-" not in string:
            format_str = "%H:%M:%S"
            to_type = "timedelta"
        elif str_len == 19:
            format_str = "%Y-%m-%d %H:%M:%S"
            to_type = "datetime"
        elif str_len == 14:
            format_str = "%Y%m%d%H%M%S"
            to_type = "datetime"
        elif str_len == 10:
            format_str = "%Y-%m-%d"
            to_type = "date"
        elif str_len == 8:
            if string[2] == ":":
                format_str = "%H:%M:%S"
                to_type = "time"
            else:
                format_str = "%Y%m%d"
                to_type = "date"
        elif str_len == 6:
            format_str = "%H%M%S"
            to_type = "time"
        elif str_len == 4:
            format_str = "%Y"
            to_type = "date"
        else:
            return string

    # Get time format by parameter 'to_type'.
    else:
        if format_str == None:
            format_dir = {
                "datetime": "%Y-%m-%d %H:%M:%S",
                "date": "%Y-%m-%d",
                "time": "%H:%M:%S",
                "timestamp": "%Y-%m-%d %H:%M:%S",
                "timedelta": "%H:%M:%S"
            }
            format_str = format_dir[to_type]

    # Additional processing timedelta type.
    if to_type == "timedelta":
        if " " in string:
            strings = string.split(" ")
            day_str, string = strings[0], strings[-1]
        else:
            day = "0"
        try:
            day = int(day_str)
        except ValueError:
            if throw_error:
                raise ValueError("failed to format string as time object")
            return string

    # Convert to time type.
    try:
        time_obj = datetime.datetime.strptime(string, format_str)
    except ValueError:
        if throw_error:
            raise ValueError("failed to format string as time object")
        return string
    if to_type == "date":
        time_obj = time_obj.date()
    elif to_type == "time":
        time_obj = time_obj.time()
    elif to_type == "timestamp":
        time_obj = int(time_obj.timestamp() * 1000)
    elif to_type == "timedelta":
        second = time_obj.second
        second += day * 86400
        time_obj = datetime.timedelta(seconds=second)

    return time_obj

@overload
def is_sql_time(content: Union[str, int], return_datatime: bool = False) -> Union[bool, datetime.datetime]: ...

@overload
def is_sql_time(return_datatime: Literal[False]) -> bool: ...

@overload
def is_sql_time(return_datatime: Literal[True]) -> datetime.datetime: ...

def is_sql_time(
    content: Union[str, int],
    return_datatime: bool = False
) -> Union[bool, datetime.datetime]:
    """
    Judge whether it conforms to SQL time format.

    Parameters
    ----------
    content : Judge object.
    return_datatime : Whether return datetime object.

    Returns
    -------
    Judgment result or transformed values.
    """

    # Extract number string.

    ## From str object.
    if type(content) == str:
        content_len = len(content)
        if content_len < 5:
            return False
        if is_number_str(content[4]):
            if content_len == 8:
                datetimes_str = [content[0:4], content[4:6], content[6:8], None, None, None]
            else:
                pattern = "^(\d{2}|\d{4})(\d{2})(\d{1,2})(\d{0,2})(\d{0,2})(\d{0,2})$"
                result = re_search(pattern, content)
                datetimes_str = list(result)
        else:
            pattern = "^(\d{2}|\d{4})[\W_](\d{2})[\W_](\d{2})[\W_]?(\d{2})?[\W_]?(\d{2})?[\W_]?(\d{2})?$"
            result = re_search(pattern, content)
            datetimes_str = list(result)

    ## From int object.
    elif type(content) == int:
        content = str(content)
        content_len = len(content)
        if content_len < 3:
            return False
        elif content_len <= 8:
            pattern = r"^(\d{0,4}?)(\d{1,2}?)(\d{2})$"
            result = re_search(pattern, content)
            datetimes_str = list(result)
            datetimes_str += [None, None, None]
        else:
            pattern = r"^(\d{0,4}?)(\d{1,2})(\d{2})(\d{2})(\d{2})(\d{2})$"
            result = re_search(pattern, content)
            datetimes_str = list(result)

    # Judge.
    year_len = len(datetimes_str[0])
    datetimes_str[0] = "2000"[0:4-year_len] + datetimes_str[0]
    year, month, day, hour, minute, second = [
        0 if int_str in ["", None] else int(int_str)
        for int_str in datetimes_str
    ]
    try:
        datetime.datetime(year, month, day, hour, minute, second)
    except ValueError:
        return False

    # Return datatime object.
    if return_datatime:
        return datetime.datetime(year, month, day, hour, minute, second)

    return True

class RDateTimeMark():
    """
    Rey's date time mark type.
    """

    def __init__(self) -> None:
        """
        Mark now time.
        """

        # Marking.
        self.mark()

    def mark(self) -> Dict[
        Literal["index", "timestamp", "datetime", "datetime_str", "interval_timestamp", "interval_timedelta", "interval_timedelta_str"],
        Optional[Union[str, float, datetime.datetime, datetime.timedelta]]
    ]:
        """
        Mark now time and return mark time information.

        Returns
        -------
        Mark time information.
        """

        # Compatible with first marking.
        if "record" not in self.__dir__():
            self.record = []

        # Get parametes.
        record_len = len(self.record)
        mark_info = {
            "index": record_len,
            "timestamp": now("timestamp"),
            "datetime": now("datetime"),
            "datetime_str": now(),
        }

        # Marking.

        ## First.
        if record_len == 0:
            mark_info["interval_timestamp"] = None
            mark_info["interval_timedelta"] = None
            mark_info["interval_timedelta_str"] = None

        ## Non first.
        else:
            last_datetime = self.record[-1]["datetime"]
            last_timestamp = self.record[-1]["timestamp"]
            mark_info["interval_timestamp"] = mark_info["timestamp"] - last_timestamp
            mark_info["interval_timedelta"] = mark_info["datetime"] - last_datetime
            mark_info["interval_timedelta_str"] = time_to_str(mark_info["interval_timedelta"])

        self.record.append(mark_info)

        return mark_info

    def report(self) -> DataFrame:
        """
        Print and return mark time information.

        Returns
        -------
        DataFrame object of pandas package with mark time information.
        """

        # Get parameters.
        data = [
            {
                "timestamp": row["timestamp"],
                "datetime": row["datetime_str"],
                "interval": row["interval_timedelta_str"]
            }
            for row in self.record
        ]

        # Generate report.
        report_df = DataFrame(data)
        interval_timedelta = self.record[-1]["datetime"] - self.record[0]["datetime"]
        interval = time_to_str(interval_timedelta)
        sum_df = DataFrame({"interval": interval}, index = ["sum"])
        report_df = pd_concat([report_df, sum_df])
        report_df.fillna("-", inplace=True)

        # Report.
        title = "Time Mark"
        rprint(report_df, title=title)

        return report_df