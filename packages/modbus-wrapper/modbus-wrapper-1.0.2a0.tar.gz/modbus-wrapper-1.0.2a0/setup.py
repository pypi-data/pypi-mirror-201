#!/usr/bin/env python

from setuptools import setup

setup(name='modbus-wrapper',
    version='1.0.2a',
    description='wrapper for pyModbusTCP accepting all Modbus numbers with Fatek support',
    author='Przemyslaw Bubas',
    author_email='bubasenator@gmail.com',
    url='https://github.com/pbubas/modbus_wrapper',
    install_requires=['pyModbusTCP'],
    keywords="modbus fatek",
     )