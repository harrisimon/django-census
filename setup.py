"""Sets up the package"""

#!/usr/bin/env python
 # -*- coding: utf-8 -*-


from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE.md') as f:
    LICENSE = f.read()

setup(
    name='django-auth',
    version='0.1.0',
    description='Django Census',
    long_description=README,
    author='<author>',
    author_email='<email>',
    url='',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)
