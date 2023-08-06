import re

from setuptools import find_packages, setup

NAME = "botdata"

VERSIONFILE = "botdata/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name=NAME,
    packages=find_packages(include=["botdata", "botdata.*"]),
    version=verstr,
    description="BOT Data is a Python package for retrieving data from the website of the Bank of Thailand",
    long_description="BOT Data is a Python package for retrieving data from the website of the Bank of Thailand",
    author="Fintech (Thailand) Company Limited",
    author_email="admin@fintech.co.th",
    url="https://github.com/ezyquant/BOT-Data",
    maintainer="Fintech (Thailand) Company Limited",
    maintainer_email="admin@fintech.co.th",
    python_requires=">=3.8",
    install_requires=["pandas>=1.3", "lxml>=4.0"],
    license="The MIT License (MIT)",
    classifiers=[
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Documentation": "https://github.com/ezyquant/BOT-Data",
        "Bug Reports": "https://github.com/ezyquant/BOT-Data/issues",
        "Source": "https://github.com/ezyquant/BOT-Data",
    },
)
