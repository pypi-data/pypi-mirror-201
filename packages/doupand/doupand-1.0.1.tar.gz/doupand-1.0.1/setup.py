# -*-coding: utf-8 -*-
# @Time    : 2023/4/8 02:39
# @Description  : PIPY INFO

from setuptools import find_packages, setup
import doupand

long_desc = """
DouPand
===============

* easy to use as most of the data returned are pandas DataFrame objects
* can be easily saved as csv, excel or json files
* can be inserted into MySQL or Mongodb

Target Users
--------------

* financial market analyst of China
* learners of financial data analysis with pandas/NumPy
* people who are interested in China financial data

Installation
--------------

    pip install doupand

Upgrade
---------------

    pip install doupand --upgrade

Quick Start
--------------

::

    import doupand as dp

    print(dp.datareader.ashare_description())

return::

          s_dp_code  s_code  ... s_exchmarket s_listboard
    0     000001.SZ  000001  ...         SZSE          主板
    1     000002.SZ  000002  ...         SZSE          主板
    2     000003.SZ  000003  ...         SZSE          主板
    3     000004.SZ  000004  ...         SZSE          主板
    4     000005.SZ  000005  ...         SZSE          主板
    ...         ...     ...  ...          ...         ...
    5329  873169.BJ  873169  ...          BSE         北交所
    5330  873223.BJ  873223  ...          BSE         北交所
    5331  873305.BJ  873305  ...          BSE         北交所
    5332  873339.BJ  873339  ...          BSE         北交所
    5333  873527.BJ  873527  ...          BSE         北交所
"""

setup(
    name='doupand',
    version=doupand.__version__,
    description='A simple and easy-to-use financial data interface library built for normal investors!',
    long_description=long_desc,
    author='DouBro',
    author_email='doupand@163.com',
    packages=find_packages(),
    platforms=["all"],
    license='BSD',
    keywords='Financial Data Interface',
    url='https://doupand.com',
    install_requires=["pandas", "requests"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: BSD License'
    ],
    include_package_data=True,
    package_data={'': ['*.csv', '*.txt']},
)
