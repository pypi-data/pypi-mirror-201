# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='budibase client',
    version='0.1.1',
    description='A lightweight client for budibase',
    long_description=readme,
    author='Nick Schulze',
    author_email='nick.schulze@uk-koeln.de',
    #url='https://github.com/kennethreitz/samplemod',
    license='MIT',
    url='https://gitlab.com/idcohorts/Python-Packages/budibase-python-client',
    packages=['budibase_client'],
    keywords=['budibase', 'client', 'api'],
    install_requires=install_requires,
)
