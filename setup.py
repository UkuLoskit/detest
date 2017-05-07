# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='detest',
    version='0.0.1',
    description='Detest unit test parser',
    long_description=readme,
    author='Uku Loskit',
    author_email='ukuloskit@gmail.com',
    url='https://github.com/UkuLoskit/detest',
    license=license,
    packages=find_packages(exclude=('tests'))
)
