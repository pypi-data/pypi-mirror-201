#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: 文件.py
# Mail: 1957875073@qq.com
# Created Time:  2022-4-25 10:17:34
# Description: 有关 文件 的自动化操作
#############################################
import pypistats
from pprint import pprint


def pip_times(package_name):
    """
    下载次数
    """
    print(pypistats.recent(package_name))


def python_version(package_name):
    """
    python版本
    """
    print(pypistats.python_minor(package_name))


def system(package_name):
    """
    下载系统
    """
    print(pypistats.system(package_name))


if __name__ == '__main__':
    print(666)
    r = pypistats.recent('poocr')
    print(type(r))
