#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import annotations

import os
from configparser import RawConfigParser
from typing import Optional


APP = "APP"
package = "package"
IME = "IME"
default_ime = "default_ime"


class ReadConfig:
    """配置文件读取类

    读取 ini 格式的配置文件

    Usage:
        config = ReadConfig('path/to/config.ini')
        package_name = config.package_name
        default_ime = config.default_ime
    """

    def __init__(self, path: str) -> None:
        """初始化配置读取器

        Args:
            path: 配置文件路径

        Raises:
            FileNotFoundError: 配置文件不存在
        """
        self.path = path
        if not os.path.exists(path):
            raise FileNotFoundError(f"配置文件不存在: {path}")

        self._config = RawConfigParser()
        self._config.read(path, encoding='utf-8')

    def _get(self, section: str, option: str) -> str:
        """获取配置项

        Args:
            section: 配置段落
            option: 配置项

        Returns:
            配置值
        """
        return self._config.get(section, option)

    def get(self, section: str, option: str, fallback: Optional[str] = None) -> Optional[str]:
        """获取配置项（带默认值）

        Args:
            section: 配置段落
            option: 配置项
            fallback: 默认值

        Returns:
            配置值或默认值
        """
        return self._config.get(section, option, fallback=fallback)

    @property
    def package_name(self) -> str:
        """获取应用包名"""
        return self._get(APP, package)

    @property
    def default_ime(self) -> str:
        """获取默认输入法"""
        return self._get(IME, default_ime)


if __name__ == '__main__':
    pass