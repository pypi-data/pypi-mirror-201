#!/usr/bin/python
# -*- coding:utf-8 _*-
"""
@author:TXU
@file:allure_label_dynamic
@time:2023/04/02
@email:tao.xu2008@outlook.com
@description:
__init__.py文件包含内容：
    __module_zh__ = 'XXX'
"""
import os
import re
import ast


class ModuleDefineInit(object):
    """ 获取__init__.py中 __module_zh__ """
    def __init__(self):
        pass

    @staticmethod
    def get_testcase_path_parts(tc_py, testcase_basename=''):
        """
        获取测试用例的路径 切片
        :param testcase_basename: testcase_basename
        :param tc_py: 测试用例test_*.py文件路径
        :return:
        """
        path_parts = []
        while True:
            dirname, basename = os.path.split(tc_py)
            path_parts.insert(0, basename)
            if basename in [testcase_basename]:  # , "testcase", "tests"
                path_parts.insert(0, dirname)
                break
            if dirname == "":
                # raise Exception(f"未找到*/{testcase_basename}目录！")
                return 0, None
            tc_py = dirname
        return 1, path_parts

    @staticmethod
    def get_init_module_zh(init_py):
        """
        获取包 __init__.py中：__module_zh__ = "模块中文描述"
        :param init_py: __init__.py文件路径
        :return:
        """
        module_zh_re = re.compile(r'__module_zh__\s+=\s+(.*)')
        with open(init_py, 'rb') as f:
            ret = module_zh_re.search(f.read().decode('utf-8'))

        if ret:
            str_zh = ret.group(1)
            module_zh = str(ast.literal_eval(str_zh)).strip()
            return module_zh
        # print(f"{init_py} 未定义：__module_zh__")
        return ret

    def get_testcase_module_list(self, tc_py_path, testcase_basename):
        module_list = []
        testcase_idx, path_parts = self.get_testcase_path_parts(tc_py_path, testcase_basename)
        if not path_parts:
            return module_list
        testcase_path = os.path.join(*path_parts[:testcase_idx])
        part_path = testcase_path
        for idx, part in enumerate(path_parts[testcase_idx:]):
            part_path = os.path.join(part_path, part)
            init_py_path = os.path.join(part_path, '__init__.py')
            if not os.path.exists(init_py_path):
                continue
            module_zh = self.get_init_module_zh(init_py_path)
            if module_zh:
                module_list.append(module_zh)
        return module_list


if __name__ == '__main__':
    pass
