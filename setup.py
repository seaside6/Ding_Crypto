# -*- coding:utf-8 -*-
from distutils.core import setup
#from setuptools import setup, find_packages

setup(
    name = 'DingCrypto',
    version = '0.1',

    keywords = ('ding', 'crypto'),
    description = 'Dingtalk Crypto',

    author = 'seaside6',
    author_email = 'lht166@163.com',
    url='https://github.com/seaside6/Ding_Crypto.git',

    packages = ['DingCrypto'],
    install_requires=['pycrypto'],
    license = 'MIT',
    platforms = 'any'
)