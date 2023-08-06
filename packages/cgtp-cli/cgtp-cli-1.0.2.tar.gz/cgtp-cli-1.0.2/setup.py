# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""


import re
from setuptools import setup, find_packages


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('cgtp_cli/cli.py').read(),
    re.M
).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name="cgtp-cli",
    packages=find_packages(),
    py_modules=['cgtp_cli', 'cgtp_cli.cli'],
    entry_points={
        "console_scripts": ['cgtp_cli = cgtp_cli.cli:main']
    },
    version=version,
    description="This is a command line application that allows you to ask ChatGPT about a command you need.",
    long_description=long_descr,
    author="Edwinsn",
    author_email="edwinsanchez750@gmail.com",
    install_requires=[requirements],
    # url = "https://github.com/edwinsn/cgtp_cli",
)