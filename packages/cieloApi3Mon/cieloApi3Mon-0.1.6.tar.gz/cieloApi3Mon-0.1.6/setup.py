#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

settings = dict()


# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

settings.update(
    name='cieloApi3Mon',
    version='0.1.6',
    description='SDK API-3.0 Python Cielo Atualizada',
    author='Monetizze',
    author_email='suporte@monetizze.com.br',
    url='https://github.com/Monetizze/API-3.0-Python',
    keywords='api3.0 cielo python sdk ecommerce',
    packages=find_packages(),
    install_requires=['requests', 'future'],
    license='MIT',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    )
)


setup(**settings)