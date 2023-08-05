#!/usr/bin/env python

import io

from setuptools import setup, find_packages


setup(
    name='iregexp',
    version='0.6.0',
    description='I-Regexp push-down automaton checker',
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Springcomp',
    author_email='springcomp@users.noreply.github.com',
    url='https://github.com/springcomp/python-iregexp',
    packages=find_packages(exclude=['tests']),
    license='MIT',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)