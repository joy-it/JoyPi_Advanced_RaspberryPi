import setuptools
from distutils.core import setup
from codecs import open
from os import path


setuptools.setup(
    name="JoyPiAdvanced",
    setup_requires=["setuptools_scm"],
    description="Library for the use of the Joy Pi Advanced",
    author="Joy-IT",
    license="MIT",
    packages=setuptools.find_packages()
)