#!/usr/bin/env python
"""
userlex
"""

from setuptools import find_packages, setup
import os

install_requires = []
tests_requires = ["pytest", "flake8"]

with open("README.md", "r") as fh:
    long_description = fh.read()

base_dir = os.path.dirname(__file__)

version = {}
with open(os.path.join(base_dir, "userlex", "__about__.py")) as fp:
    exec(fp.read(), version)

setup(
    name="userlex",
    version=version["__version__"],
    author="Danila Vershinin",
    author_email="info@getpagespeed.com",
    url="https://github.com/dvershinin/userlex",
    description="A library to extract social media and other useful things",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    license="BSD",
    install_requires=install_requires,
    extras_require={
        "tests": install_requires + tests_requires,
    },
    tests_require=tests_requires,
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers"
    ],
)
