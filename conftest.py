#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import annotations

import time
import pytest
from airtest.core.api import connect_device
from py.xml import html

from core.aircore import AirtestPoco, d


@pytest.fixture(scope='session', autouse=True)
def init_airtest_poco():
    """初始化 AirtestPoco 全局实例"""
    device = connect_device("android:///")
    global d
    d = AirtestPoco(device)
    yield d
    # teardown: 可在此处清理资源


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """当测试失败时，自动截图并展示到 HTML 报告中"""
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when in ('call', 'setup'):
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            if d:
                screen_img = d.capture_screenshot()
                if screen_img:
                    extra.append(pytest_html.extras.html(
                        f'<div><img src="data:image/png;base64,{screen_img}" '
                        f'alt="screenshot" style="width:300px;height:600px;" '
                        f'onclick="window.open(this.src)" align="right"/></div>'
                    ))
    report.extra = extra
    report.description = str(item.function.__doc__)


@pytest.hookimpl
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


@pytest.hookimpl
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('passed.', class_='empty log'))


@pytest.hookimpl
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("所属部门: 测试")])
    prefix.extend([html.p("测试执行人: 侯伟轩")])


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """收集并打印测试结果统计"""
    result = {
        "total": terminalreporter._numcollected,
        'passed': len(terminalreporter.stats.get('passed', [])),
        'failed': len(terminalreporter.stats.get('failed', [])),
        'error': len(terminalreporter.stats.get('error', [])),
        'skipped': len(terminalreporter.stats.get('skipped', [])),
        'total times': time.time() - terminalreporter._sessionstarttime
    }
    print(result)