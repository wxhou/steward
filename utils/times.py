#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import annotations

import time
import datetime
from typing import Optional

from airtest.report.report import timefmt as airtest_timefmt
from airtest.core.api import sleep as airtest_sleep


def timestamp() -> float:
    """获取当前时间戳"""
    return time.time()


def strftime(fmt: str = "%Y%m%d%H%M%S") -> str:
    """格式化时间字符串

    Args:
        fmt: 时间格式，默认 "%Y%m%d%H%M%S"

    Returns:
        格式化后的时间字符串
    """
    return time.strftime(fmt, time.localtime())


def now_time() -> datetime.datetime:
    """获取当前时间"""
    return datetime.datetime.now()


def timefmts() -> str:
    """获取格式化时间戳字符串"""
    return airtest_timefmt(timestamp())


def sleep(seconds: float) -> None:
    """等待指定秒数

    Args:
        seconds: 等待时间（秒）
    """
    airtest_sleep(seconds)


if __name__ == '__main__':
    print(strftime())