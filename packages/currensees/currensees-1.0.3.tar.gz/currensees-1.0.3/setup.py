# coding: utf-8

import sys
from setuptools import setup, find_packages  # noqa: H301
from distutils.core import Extension

NAME = "currensees"
VERSION = "1.0.3"
REQUIRES = ["requests"]

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'LONG_DESCRIPTION.rst')) as f:
    long_description = f.read()

macros = []
if sys.platform.startswith('freebsd') or sys.platform == 'darwin':
    macros.append(('PLATFORM_BSD', '1'))
elif 'linux' in sys.platform:
    macros.append(('_GNU_SOURCE', ''))

setup(
    name=NAME,
    version=VERSION,
    description="Python library for integrating with the Currency API.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Moat Systems Limited",
    author_email="support@moatsystems.com",
    url="https://moatsystems.com/currency-api/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRES,
    zip_safe=False,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    project_urls={
        "Bug Tracker": "https://github.com/moatsystems/currensees_sdk/issues",
        "Changes": "https://github.com/moatsystems/currensees_sdk/blob/main/CHANGELOG.md",
        "Documentation": "https://docs.currensees.com/",
        "Source Code": "https://github.com/moatsystems/currensees_sdk",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=["wheel"],
    keywords=["currency",
              "currency api",
              "currensees",
              "currensees sdk",
              "rate",
              "rates",
              "exchange rates",
              "moat",
              "moatsystems",
              "moat systems"],
    license='BSD 3-Clause',
)