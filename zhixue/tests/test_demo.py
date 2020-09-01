#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from utils.times import sleep
from core.aircore import d


class TestZhiXue:

    def test_001(self):
        """进行登录操作"""
        d.poco_click(name="com.iflytek.elpmobile.smartlearning:id/account_login_tv")
        d.poco_set_text("", name="com.iflytek.elpmobile.smartlearning:id/login_name")
        d.poco_set_text('18291900215', name="com.iflytek.elpmobile.smartlearning:id/login_name")
        d.poco_set_text("", name="com.iflytek.elpmobile.smartlearning:id/login_pwd")
        d.poco_set_text('test001', name="com.iflytek.elpmobile.smartlearning:id/login_pwd")
        d.poco_click(name="com.iflytek.elpmobile.smartlearning:id/login_btn")
        sleep(8)

    def test_002(self):
        """进行登出操作"""
        d.poco_click(text="我的")
        d.poco_click(name="com.iflytek.elpmobile.smartlearning:id/head_collect")
        d.poco_click(name="com.iflytek.elpmobile.smartlearning:id/btn_user_exit")
        d.poco_click(name="com.iflytek.elpmobile.smartlearning:id/dialog_right")
        sleep(5)


if __name__ == '__main__':
    pytest.main('test_demo.py')
