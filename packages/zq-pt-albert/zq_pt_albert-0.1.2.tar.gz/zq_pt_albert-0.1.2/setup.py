#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='zq_pt_albert',
    version='0.1.2',
    description=(
        'google small zh albert tf'
    ),
    author='zhangqi',
    author_email='zhangqi23@163.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'xlrd==1.2.0',
        'xlwt',
        'xlutils',
        'configparser',
        'xlsxwriter==3.0.1',
        'tqdm'
    ],
)
