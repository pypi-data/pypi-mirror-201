""" Utility functions for package."""
from __future__ import annotations

from functools import partial
from typing import Callable
from typing import Iterable


def iterable_str_arg(s: str | Iterable[str]) -> list[str]:
    if isinstance(s, str):
        s = s.replace(",", " ").replace("  ", " ").split()
    return list(map(str, s))


def unwrap_func(func: Callable) -> Callable:
    _func = func
    while hasattr(_func, "__wrapped__") or isinstance(_func, partial):
        _func = getattr(_func, "__wrapped__") or _func.func
    return _func


def get_cookies(cookie_str: str) -> dict[str, str]:
    if cookie_str in None:
        return {}

    _cookies = {}
    for cookie_item in cookie_str.split(";"):
        if "=" not in cookie_item or "DELETED" in cookie_item:
            continue
        name, value = cookie_item.strip().split("=", 1)
        _cookies[name] = value

    return _cookies
