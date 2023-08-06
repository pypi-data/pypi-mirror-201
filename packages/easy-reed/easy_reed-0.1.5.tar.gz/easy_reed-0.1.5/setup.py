#!/usr/bin/env python
from setuptools import setup, find_packages

setup_info = dict(
  name='easy_reed',
  python_requires=">=3.7",
  version='0.1.5',
  description='Config Library for cross module configuration',
  author="Reed Schick",
  author_email='rns350@nyu.edu',
  url='https://github.com/rns350/easy-reed',
  packages=find_packages(
    where='.', 
    include=['easy_reed*']
  ),
  install_requires=[],
  setup_requires=[],
  tests_require=['pytest']
)

setup(**setup_info)