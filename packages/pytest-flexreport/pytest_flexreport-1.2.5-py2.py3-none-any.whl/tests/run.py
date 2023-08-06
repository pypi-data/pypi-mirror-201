#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TXU
@file:run.py
@time:2023/1/31
@email:tao.xu2008@outlook.com
@description: 
"""
import json
import pytest


def main(template_id=2):
    # - 构建pytest 参数
    print("构建pytest 参数...")
    pytest_files_set = [
        './tests/test_demo1.py',
        './tests/test_demo2.py',
        './tests/test_demo3.py'
    ]
    argv = pytest_files_set + [
        # pytest-testreport
        f'--template={template_id}',
        f'--report=./reports/template{template_id}',
        '--history_dir=./reports/',
        '--title=测试报告：demo（ID=xxx）',
        '--tester=txu',
        '--desc=demo-demo-demo-demo',
        '--log_path=./reports/',
        '--report_path=./reports/',
        '--testcase_basename=tests',
        # '--report_sort',

    ]
    print("pytest 命令：{}\n".format(json.dumps(argv, indent=2)))

    pytest.main(argv)


if __name__ == '__main__':
    # main(1)
    # main(2)
    main(3)
