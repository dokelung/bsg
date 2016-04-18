#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

setup(
    name='bsg',
    version='0.1.dev',
    description="Simple BeautifulSoup web gui",
    long_description=readme,
    author="dokelung",
    author_email='dokelung@gmail.com',
    url='https://github.com/dokelung/bsg',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='Beautiful Soup',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
)
