# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# This call to setup() does all the work
setup(
    name="marfa_bi_connection",
    version="1.0.6",
    description="MarfaBI connections",
    url="https://github.com/NorddyM/MarfaBI",
    author="Ruslan Galimov",
    author_email="rgalimov@marfa-tech.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["marfa_bi_connection"],
    include_package_data=True,
    install_requires=['PyMySQL',
                      'PyYAML',
                      'sshtunnel',
                      'pandas==1.5.3',
                      'python-telegram-bot==13.15',
                      'SQLAlchemy==2.0.6',
                      'clickhouse-sqlalchemy',
                      'clickhouse-driver',
                      'google-cloud-bigquery',
                      'slack-sdk',
                      'google',
                      'cryptography']
)