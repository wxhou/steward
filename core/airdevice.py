#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import annotations

from typing import Optional, Tuple

from airtest.core.android.android import Android
from airtest.core.android.constant import YOSEMITE_IME_SERVICE


class AirDevice:
    """Android 设备操作类"""

    _instance: Optional['AirDevice'] = None

    def __new__(cls, *args, **kwargs):
        """单例模式，确保只有一个设备实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, serialno: Optional[str] = None, adb_path: Optional[str] = None):
        if self._initialized:
            return

        self._android: Optional[Android] = None
        self._serialno = serialno
        self._adb_path = adb_path
        self._initialized = True

    @property
    def android(self) -> Android:
        """延迟初始化 Android 实例"""
        if self._android is None:
            self._android = Android(serialno=self._serialno, adb_path=self._adb_path)
        return self._android

    @property
    def adb(self):
        """获取 ADB 实例"""
        return self.android.adb

    @property
    def screen(self) -> Tuple[int, int]:
        """获取屏幕分辨率 (width, height)"""
        info = self.android.display_info
        return info.get('width'), info.get('height')

    @property
    def device_id(self) -> str:
        """获取设备 ID"""
        return self.android.uuid

    @property
    def get_top_activity(self) -> str:
        """获取当前顶级 Activity"""
        return self.android.get_top_activity()

    @property
    def get_default_ime(self) -> str:
        """获取默认输入法"""
        return self.adb.shell("settings get secure default_input_method").strip()

    @property
    def get_ipv4(self) -> Optional[str]:
        """获取设备 IPv4 地址"""
        return self.android.get_ip_address()

    def close_yosemite_ime(self, ime: str) -> None:
        """关闭 Yosemite 输入法，切换到指定输入法"""
        self.adb.shell(f"ime disable {YOSEMITE_IME_SERVICE}")
        self.adb.shell(f"ime set {ime}")

    @classmethod
    def reset(cls) -> None:
        """重置单例实例（用于测试或重新连接）"""
        cls._instance = None


# 延迟实例化
def get_airdev(serialno: Optional[str] = None, adb_path: Optional[str] = None) -> AirDevice:
    """获取 AirDevice 实例"""
    if serialno or adb_path:
        return AirDevice(serialno=serialno, adb_path=adb_path)
    if AirDevice._instance is None:
        AirDevice._instance = AirDevice()
    return AirDevice._instance


# 为了向后兼容，提供一个全局实例
airDev: Optional[AirDevice] = None


def _lazy_init_airdev():
    """延迟初始化全局 airDev"""
    global airDev
    if airDev is None:
        airDev = AirDevice()
    return airDev


# 注：实际初始化在需要时通过 get_airdev() 进行
# 不再在模块加载时自动初始化


__all__ = ['AirDevice', 'airDev', 'get_airdev']