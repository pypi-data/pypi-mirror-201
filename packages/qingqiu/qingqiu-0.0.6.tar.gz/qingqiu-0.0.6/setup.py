#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lixuecheng
# Mail: lixuechengde@163.com
# Created Time: 2022年3月8日
#############################################


from setuptools import setup, find_packages



setup(
name = "qingqiu",
version = "0.0.6",
keywords = ["pip", "easy","requests","auto"],
description = "简单得接口测试框架",
long_description = "简单得接口测试框架",
license = "MIT Licence",

url = "https://gitee.com/tuboyou/qingqiu",
author = "lixuecheng",
author_email = "lixuechengde@163.com",
packages = find_packages(),
include_package_data = True,
platforms = "any",
install_requires = ['requests','pytest','pytest-rerunfailures','pytest-html','pytest-dependency','json-tools'],
py_modules=['qingqiu'],
entry_points={
'console_scripts': ['qing=qingqiu.qing:qing']
},
classifiers = [
'Intended Audience :: Developers',
'Topic :: Software Development :: User Interfaces',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3.5',
'Programming Language :: Python :: 3.6',
'Programming Language :: Python :: 3.7',
'Programming Language :: Python :: 3.8',
'Programming Language :: Python :: 3.9',
'Programming Language :: Python :: 3.10',
'Programming Language :: Python :: 3.11',
],
python_requires='>=3.5',
)
