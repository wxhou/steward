#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import pytest
from core.aircore import *
from py._xmlgen import html


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            screen_img = d.capture_screenshot()
            if screen_img:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:300px;height:600px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.description = str(item.function.__doc__)


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('passed.', class_='empty log'))


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("所属部门: 测试")])
    prefix.extend([html.p("测试执行人: 侯伟轩")])


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """收集测试结果"""
    result = {
        "total": terminalreporter._numcollected,
        'passed': len(terminalreporter.stats.get('passed', [])),
        'failed': len(terminalreporter.stats.get('failed', [])),
        'error': len(terminalreporter.stats.get('error', [])),
        'skipped': len(terminalreporter.stats.get('skipped', [])),
        'total times': time.time() - terminalreporter._sessionstarttime
    }
    print(result)
