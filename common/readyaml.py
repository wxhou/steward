#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import annotations

import os
from typing import Any

import yaml


class ReadYaml:
    """YAML 文件读取类

    Usage:
        data = ReadYaml('path/to/element', 'page_data')
        activity_list = data['活动报名']
        first_activity = data['活动报名'][0]
    """

    def __init__(self, route: str, name: str) -> None:
        """初始化 YAML 读取器

        Args:
            route: YAML 文件所在目录
            name: YAML 文件名（不含 .yaml 扩展名）
        """
        self.path = os.path.join(route, f"{name}.yaml")
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"YAML 文件不存在: {self.path}")

        with open(self.path, encoding='utf-8') as f:
            self._data: dict = yaml.safe_load(f) or {}

    def __getitem__(self, item: str) -> Any:
        """获取 YAML 数据

        Args:
            item: 键名

        Returns:
            对应的值
        """
        return self._data[item]

    def get(self, item: str, default: Any = None) -> Any:
        """获取 YAML 数据（带默认值）

        Args:
            item: 键名
            default: 默认值

        Returns:
            对应的值或默认值
        """
        return self._data.get(item, default)


if __name__ == '__main__':
    pass