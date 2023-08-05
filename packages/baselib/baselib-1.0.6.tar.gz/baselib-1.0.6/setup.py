# -*- coding:utf-8 -*-
# from distutils.core import setup
from setuptools import find_packages
from setuptools import setup

setup(
    name='baselib',
    version="1.0.6",
    description='base common lib for python',
    author='coreylam',
    author_email='coreylam@163.com',
    url='https://github.com/coreylam/base_common_lib',
    license='GPL',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[]
)
