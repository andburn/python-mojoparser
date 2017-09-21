#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='mojoparser',
    version='0.1.0',
    author='andburn',
    url='https://github.com/andburn/python-mojoparser',
    packages=find_packages(exclude=('tests',)),
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)
