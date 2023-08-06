import ast
from datetime import date, datetime
from typing import Union

import dateparser


def date_validator(obj: Union[date, str]) -> date:
    try:
        if isinstance(obj, date):
            date_obj = obj
        
        elif isinstance(obj, str):
            date_obj = dateparser.parse(obj).date()

    except (TypeError, ValueError):
        raise TypeError(f"{obj} cannot be turned into a date type!")

    return date_obj


def datetime_validator(obj: Union[datetime, str]) -> datetime:
    try:
        if isinstance(obj, datetime):
            datetime_obj = obj
        
        elif isinstance(obj, str):
            datetime_obj = dateparser.parse(obj)

    except (TypeError, ValueError):
        raise TypeError(f"{obj} cannot be turned into a datetime type!")

    return datetime_obj


def dict_validator(obj: Union[dict, str]) -> dict:
    try:
        if isinstance(obj, dict):
            dict_obj = obj
        
        elif isinstance(obj, str):
            dict_obj = ast.literal_eval(obj)

    except (TypeError, ValueError):
        raise TypeError(f"{obj} cannot be turned into a dict type!")

    return dict_obj


def list_validator(obj: Union[list, str]) -> list:
    try:
        if isinstance(obj, list):
            list_obj = obj
        
        elif isinstance(obj, str):
            list_obj = ast.literal_eval(obj)

    except (TypeError, ValueError):
        raise TypeError(f"{obj} cannot be turned into a list type!")

    return list_obj


def integer_validator(obj) -> int:
    if isinstance(obj, int):
        return obj

    else:
        raise TypeError(f"{obj} must be integer type!")


def float_validator(obj) -> float:
    if isinstance(obj, float):
        return obj

    else:
        raise TypeError(f"{obj} must be float type!")


def string_validator(obj) -> str:
    if isinstance(obj, str):
        return obj

    else:
        raise TypeError(f"{obj} must be string type!")


def boolean_validator(obj) -> bool:
    if isinstance(obj, bool):
        return obj

    else:
        raise TypeError(f"{obj} must be boolean type!")