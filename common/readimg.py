#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from config import airImg


class ReadImg(object):
    def __init__(self, name):
        self.path = os.path.join(airImg['zhixue'], name)

    def __getitem__(self, item):
        result = os.path.join(self.path, "{}.png".format(item))
        if os.path.isfile(result):
            return result
        raise FileNotFoundError("{}不存在".format(result))


if __name__ == '__main__':
    pass
