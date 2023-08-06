#!/usr/bin/env python
from setuptools import setup, find_packages
import gpp

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="py_extension_functions",
    version=gpp.__version__,
    author="aJava",
    author_email="gaolious@gmail.com",
    description="personally, python extension functions",
    long_description_content_type='text/markdown',
    long_description=long_description,
    url="https://github.com/Gaolious/py_extension_functions",
    packages=find_packages(include=('gpp',), exclude=('__pycache__',)),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=["pytz", "Django>=3.2"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
