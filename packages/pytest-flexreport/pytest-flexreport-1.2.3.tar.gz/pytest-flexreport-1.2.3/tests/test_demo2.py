#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TXU
@file:test_demo2.py
@time:2023/1/31
@email:tao.xu2008@outlook.com
@description: 
"""
import time
import allure


@allure.epic("对象存储")
@allure.story("桶")
@allure.feature("对象")
@allure.suite("正常")
class TestDemo2(object):


    def test_1(self):
        assert 3 + 2 == 5

    def test_2(self):
        time.sleep(2)
        assert 3 + 2 == 6

    def test_3(self):
        assert 3 + 2 == 7

    def test_4(self):
        assert 3 + 2 == 5


if __name__ == '__main__':
    pass
