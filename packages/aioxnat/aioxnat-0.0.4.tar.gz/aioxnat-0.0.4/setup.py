import pathlib
from setuptools import setup, find_packages

PROJECT_ROOT = pathlib.Path(__file__).parent

# Configuration
VERSION = (0, 0, 4)
DESCRIPTION = "Asyncronous XNAT RESTful Interface"
LONG_DESCRIPTION = """\
RESTful interface, from client to XNAT, for basic operations.
"""
DEPENDENCIES = (PROJECT_ROOT / "requirements.txt").read_text().splitlines()


setup(
    name="aioxnat",
    version=".".join([str(v) for v in VERSION]),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Keenan W. Wilkinson",
    author_email="keenanwilkinson@outlook.com",
    license="MIT",
    packages=find_packages(),
    install_requires=DEPENDENCIES,
    keywords=["XNAT", "xnat", "async", "REST"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
