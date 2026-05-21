#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import annotations

import os
from typing import Optional


class ReadImg:
    """图片资源读取类

    支持按 app 动态读取图片资源

    Usage:
        # 默认使用 zhixue
        img = ReadImg('login_btn')
        filepath = img['login_btn']  # -> zhixue/images/login_btn.png

        # 指定其他 app
        img = ReadImg('login_btn', app='qujiangpool')
        filepath = img['login_btn']  # -> qujiangpool/images/login_btn.png
    """

    def __init__(self, name: str = '', app: Optional[str] = None) -> None:
        """初始化图片读取器

        Args:
            name: 图片名称（可省略，调用 __getitem__ 时再指定）
            app: 应用名称，默认从 config 读取
        """
        self.name = name
        if app is None:
            from config import airImg
            app = 'zhixue'
            self._base_path = airImg.get(app)
        else:
            from config import airImg
            self._base_path = airImg.get(app, airImg.get('zhixue'))

        if not self._base_path:
            from config import apps
            self._base_path = os.path.join(apps.get('zhixue', ''), 'images')

    def __getitem__(self, item: str) -> str:
        """获取图片路径

        Args:
            item: 图片名称（不含扩展名）

        Returns:
            图片完整路径

        Raises:
            FileNotFoundError: 图片文件不存在
        """
        result = os.path.join(self._base_path, f"{item}.png")
        if os.path.isfile(result):
            return result
        raise FileNotFoundError(f"图片不存在: {result}")


# 预定义常用 app 的图片读取器
def get_img_reader(app: str = 'zhixue') -> ReadImg:
    """获取指定 app 的图片读取器"""
    return ReadImg(app=app)


if __name__ == '__main__':
    # 测试
    img = ReadImg()
    print('Base path:', img._base_path)