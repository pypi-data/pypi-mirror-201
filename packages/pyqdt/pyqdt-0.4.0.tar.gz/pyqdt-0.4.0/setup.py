#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='pyqdt',
    version='0.4.0',
    packages=['pyqdt', 'pyqdt/technical_analysis'],
    install_requires=['pandas >= 0.25'],
    author='John Lui',
    author_email='johnlui@live.cn',
    license='LGPLv3',
    url='https://pyqdt.itsop.cc'
)
