#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import allure
from config import ini
from core.aircore import *
from core.airdevice import airDev
from utils.report import get_report, script_file

__author__ = '1084502012@qq.com'
__title__ = "智学网APP测试报告"
__desc__ = """测试用例1：登录
测试用例2：退出登录"""


@allure.epic("曲江池遗址公园")
@pytest.fixture(scope='session', autouse=True)
def set_session(request):
    """
    切换输入法
    """
    allure.step("开始测试！")

    log(airDev.device_id)
    d.api.wake()
    d.api.start_app(ini['zhixue'].package_name)

    def fn():
        d.api.stop_app(ini['zhixue'].package_name)
        airDev.close_yosemite_ime(ini['zhixue'].default_ime)  # 返回至默认的键盘
        allure.step("结束测试！")
        get_report(script_file)

    request.addfinalizer(fn)
