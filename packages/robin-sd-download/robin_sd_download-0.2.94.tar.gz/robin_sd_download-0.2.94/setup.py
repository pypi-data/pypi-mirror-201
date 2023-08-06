#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as file:
    long_description = file.read()

with open("requirements.txt") as file:
    install_requires = file.read().strip().split("\n")

# Fetch version from __version__ variable in robin_sd_download/_version.py
from robin_sd_download._version import __version__ as version


setup(
    name="robin_sd_download",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'robin-sd-download = robin_sd_download.__main__:main',
        ],
    },
    version=version,
    license="MIT",
    description="Package to download files to the Robin Radar API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Robin Radar Systems",
    author_email="it-team@robinradar.com",
    url="https://bitbucket.org/robin-radar-systems/sd-api-download-pip-package.git",
    keywords=["python", "robin", "radar", "download", "software", "sd"]
)
