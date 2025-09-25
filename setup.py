# -*- coding: utf-8 -*-
# @Time    : 2025/5/13 10:35
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@pharmaron.com
# @File    : setup.py
# @Software: PyCharm
# setup.py
from setuptools import setup, find_packages

setup(
    name='pychemkit',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pychemkit=pychemkit.cli:main']
    },
    install_requires=[
        'numpy',
        'matplotlib',
        'rdkit',  # 如果需要 AI 或分子结构功能
        'requests'  # 如果需要调用 PubChem API
    ],
)
