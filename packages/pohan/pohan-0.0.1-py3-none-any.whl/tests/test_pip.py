# -*- coding: UTF-8 -*-
'''
@Author  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2023/4/5 23:30 
@Description     ：
'''

import unittest

from popip import *


class TestPip(unittest.TestCase):

    def test_pip_times(self):
        pip_times('python-office')

    def test_python_minor(self):
        python_version('python-office')

    def test_system(self):
        system('python-office')
