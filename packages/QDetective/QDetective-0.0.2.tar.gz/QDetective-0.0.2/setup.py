# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 08:55:10 2023

@author: Suliang

Email: suliang_321@sina.com

TO: QDer, GO GO GO!

"""

from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='QDetective',  # 包名
      version='0.0.2',  # 版本号
      description='量化大侦探-数据通道',
      long_description=long_description,
      author='suliang',
      author_email='suliang_321@sina.ccom',
      url='',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )