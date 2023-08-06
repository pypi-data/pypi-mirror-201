#!/usr/bin/env python
import sys
version = sys.argv[1]
del sys.argv[1]
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='UQpyDTOs',
    version=version,
    long_description_content_type="text/markdown",
    long_description=readme,
    description="A collection of DTOs to deserialize json into UQpy classes",
    url='https://github.com/DTsapetis/UQpyDTOs',
    author="Dimitris Tsapetis",
    license='MIT',
    platforms=["OSX", "Windows", "Linux"],
    install_requires=[
        "UQpy"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)
