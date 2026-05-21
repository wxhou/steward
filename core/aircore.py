#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional

import allure
import base64
import pytesseract
from PIL import Image

from airtest.core import api
from airtest.core.cv import Template
from airtest.utils.transform import TargetPos
from airtest.core.settings import Settings as ST
from airtest.core.helper import G, set_logdir, log
from airtest.aircv import crop_image, cv2_2_pil
from airtest.core import error as airtest_exception
from poco.proxy import UIObjectProxy
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco import exceptions as poco_exception

from utils.times import timestamp
from utils.logger import clear_log, init_logging
from config import AIRTEST_LOG

if TYPE_CHECKING:
    from airtest.core.cv import Template
    from core.airdevice import AirDevice


class AirtestPoco:
    """
    Airtest 和 Poco 方法集合

    Airtest-API:
        图像识别相关操作
    Poco-Selector:
        UI 元素定位和操作
    """

    def __init__(self, device: Optional[object] = None) -> None:
        """初始化 AirtestPoco 实例"""
        clear_log(AIRTEST_LOG)
        set_logdir(AIRTEST_LOG)
        init_logging()
        self.timeout = ST.FIND_TIMEOUT
        self.api = api
        self.poco = AndroidUiautomationPoco(
            device=device,
            use_airtest_input=True,
            screenshot_each_action=False
        )
        self.UIObj = UIObjectProxy(poco=self.poco)

    @property
    def screen(self) -> tuple:
        """获取屏幕分辨率"""
        from core.airdevice import get_airdev
        return get_airdev().screen

    # ==================== Airtest Methods ====================

    @classmethod
    def temp(cls, img_name: str, rgb: bool = True, record_pos: tuple = (0.5, -0.5),
             resolution: tuple = None, target_pos: int = TargetPos.MID) -> Template:
        """图像识别模板

        Args:
            img_name: 图片路径
            rgb: 是否使用彩色识别
            record_pos: 记录坐标
            resolution: 屏幕分辨率，默认从设备获取
            target_pos: 目标位置

        Returns:
            Template 实例
        """
        if resolution is None:
            from core.airdevice import get_airdev
            resolution = get_airdev().screen
        return Template(
            r"%s" % img_name,
            target_pos=target_pos,
            record_pos=record_pos,
            resolution=resolution,
            rgb=rgb
        )

    @allure.step("元素点击")
    def touch(self, v: Template, **kwargs) -> None:
        """点击屏幕上指定位置或模板"""
        self.api.touch(v, **kwargs)

    @allure.step("输入文本")
    def text(self, text: str, enter: bool = True, **kwargs) -> None:
        """在焦点元素输入文本"""
        self.api.text(text, enter=enter, **kwargs)
        self.api.sleep()

    @allure.step("双击")
    def double_click(self, v: Template) -> None:
        """双击指定位置"""
        self.api.double_click(v)

    @allure.step("滑动")
    def swipe(self, v1, v2=None, vector=None, **kwargs):
        """滑动操作，支持从 v1 滑动到 v2 或按向量滑动"""
        if isinstance(v1, str) and v1.endswith('.png'):
            v1 = self.temp(v1)
        if isinstance(v2, str) and v2.endswith('.png'):
            v2 = self.temp(v2)
        return self.api.swipe(v1, v2, vector, **kwargs)

    @allure.step("等待元素")
    def wait(self, v: Template, **kwargs) -> None:
        """等待模板匹配成功"""
        self.api.wait(v, **kwargs)

    @allure.step("检查元素存在")
    def exists(self, v: Template) -> bool | tuple:
        """检查目标是否存在"""
        return self.api.exists(v)

    @allure.step("断言存在")
    def assert_exists(self, v: Template, msg: str = None) -> None:
        """断言目标存在"""
        self.api.assert_exists(v, msg)

    @allure.step("断言不存在")
    def assert_not_exists(self, v: Template, msg: str = None) -> None:
        """断言目标不存在"""
        self.api.assert_not_exists(v, msg)

    @allure.step("查找所有匹配")
    def find_all(self, v: Template) -> list:
        """查找所有匹配位置"""
        return self.api.find_all(v)

    def capture_screenshot(self, bs64: bool = True) -> str | None:
        """截图并转为 base64"""
        result = self.api.snapshot()
        if not result:
            return None
        filename = result.get('screen')
        if not filename:
            return None
        filepath = os.path.join(ST.LOG_DIR, filename)
        allure.attach.file(filepath, "截图" + filename, allure.attachment_type.JPG)
        if bs64:
            with open(filepath, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        return filepath

    # ==================== Poco Methods ====================

    @allure.step("Poco 等待任意元素")
    def poco_wait_any(self, objects: list) -> bool | object:
        """等待任意一个 UI 元素出现"""
        try:
            return self.poco.wait_for_any(objects, timeout=self.timeout)
        except poco_exception.PocoTargetTimeout:
            return False

    @allure.step("Poco 等待所有元素")
    def poco_wait_all(self, objects: list) -> bool:
        """等待所有 UI 元素出现"""
        try:
            self.poco.wait_for_all(objects, timeout=self.timeout)
            return True
        except poco_exception.PocoTargetTimeout:
            return False

    def poco_obj(self, **kwargs) -> UIObjectProxy:
        """获取 Poco 对象"""
        if 'index' in kwargs:
            index = kwargs.pop('index')
            ele = self.poco(**kwargs)[index]
        else:
            ele = self.poco(**kwargs)
        ele.wait_for_appearance(timeout=self.timeout)
        return ele

    @allure.step("Poco 点击元素")
    def poco_click(self, **kwargs) -> None:
        """点击 UI 元素"""
        log("点击元素：{}".format(kwargs))
        self.poco_obj(**kwargs).click()
        self.poco.sleep_for_polling_interval()

    @allure.step("Poco 点击坐标")
    def poco_click_pos(self, pos: list | tuple) -> None:
        """点击相对坐标 (0-1 范围)"""
        self.poco.click(pos)
        self.poco.sleep_for_polling_interval()

    @allure.step("Poco 获取文本")
    def poco_text(self, **kwargs) -> str | None:
        """获取元素文本"""
        txt = self.poco_obj(**kwargs).get_text()
        log("获取元素{}文本：{}".format(kwargs, txt))
        return txt

    @allure.step("Poco 设置文本")
    def poco_set_text(self, text: str, **kwargs) -> None:
        """设置元素文本"""
        self.poco_obj(**kwargs).set_text(text)

    @allure.step("Poco 获取属性")
    def poco_attr(self, name: str, **kwargs) -> any:
        """获取元素属性"""
        return self.poco_obj(**kwargs).attr(name)

    def poco_freeze(self, **kwargs) -> UIObjectProxy:
        """冻结 UI 树并获取元素"""
        with self.poco.freeze() as freeze:
            return freeze(**kwargs)

    def poco_hierarchy_dict(self) -> dict:
        """获取 UI 层次结构字典"""
        frozen_poco = self.poco.freeze()
        return frozen_poco.agent.hierarchy.dump()

    @allure.step("Poco 检查元素存在")
    def poco_exists(self, **kwargs) -> bool:
        """检查元素是否存在"""
        result = self.poco_freeze(**kwargs).exists()
        log("元素{}验证结果: {}".format(kwargs, result))
        return result

    @allure.step("Poco 滚动屏幕")
    def poco_scroll(self, direction: str = 'vertical', percent: float = 0.5, duration: float = 2.0) -> None:
        """滚动屏幕"""
        self.poco.scroll(direction=direction, percent=percent, duration=duration)

    @allure.step("Poco 滑动")
    def poco_swipe(self, p1, p2=None, direction=None, duration: float = 2.0) -> None:
        """滑动操作"""
        self.poco.swipe(p1=p1, p2=p2, direction=direction, duration=duration)

    # ==================== AirCV Methods ====================

    @allure.step("裁剪截图")
    def crop_image(self, rect: list) -> str:
        """截取屏幕指定区域

        Args:
            rect: [x_min, y_min, x_max, y_max]

        Returns:
            保存的截图路径
        """
        img = G.DEVICE.snapshot()
        crop_screen = crop_image(img, rect)
        filename = "%(time)d.jpg" % {'time': timestamp() * 1000}
        filepath = os.path.join(ST.LOG_DIR, filename)
        pil_image = cv2_2_pil(crop_screen)
        pil_image.save(filepath, quality=99, optimize=True)
        return filepath

    @allure.step("OCR 识别")
    def tesseract_string(self, filepath: str, lang: str = 'eng+chi_sim', config: str = '--psm 6') -> str:
        """识别图片中的文字

        Args:
            filepath: 图片路径
            lang: 识别语言
            config: Tesseract 配置

        Returns:
            识别的文字
        """
        im = Image.open(filepath).convert('L')
        threshold = 150
        table = [0 if i < threshold else 1 for i in range(256)]
        im = im.point(table, "1")
        result = pytesseract.image_to_string(im, lang=lang, config=config)
        return result.replace(" ", "")


# 全局实例将在 conftest.py 中初始化
d: Optional[AirtestPoco] = None


__all__ = ['AirtestPoco', 'd', 'G', 'ST', 'log', 'airtest_exception', 'poco_exception']