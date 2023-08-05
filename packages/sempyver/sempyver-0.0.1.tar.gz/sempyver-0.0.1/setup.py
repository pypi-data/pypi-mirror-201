"""
Whole setup for the SemPyVer package.
"""
import re
from setuptools import setup, find_packages


def read_version() -> str:
    """Read the version from the given _version.py file

    Returns:
        - Version string

    Raise:
        - TypeError: If the version could not be find.
    """
    with open("sempyver/_version.py", "r", encoding="utf-8") as version_file:
        version_coincidence = re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    # Now, check for the version coincidence
    if version_coincidence is None:
        raise TypeError("Couldn't find the version in the given file.")
    version = version_coincidence.group(1)
    # Return the version
    return version


setup(
    name='sempyver',
    version=read_version(),
    description='Setting up a python package',
    long_description="",  # ! TO BE ADDED
    author='Ricardo Leal',
    author_email='ricardo.lealpz@gmail.com',
    maintainer='Ricardo Leal',
    maintainer_email='ricardo.lealpz@gmail.com',
    url='',  # ! TO BE ADDED
    packages=find_packages(include=['sempyver', 'sempyver.*']),
    install_requires=[
        'click~=8.1',
        'inquirer~=3.1',
        'colorama==0.4.6',
        'faker~=17.6'
    ],
    entry_points={
        'console_scripts': ['sempyver=sempyver.__main__:run']
    }
)
