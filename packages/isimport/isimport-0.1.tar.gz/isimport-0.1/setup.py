from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1'
DESCRIPTION = 'Check required pip module for program.'
LONG_DESCRIPTION = 'A package that check required pip module to be installed on system.'

# Setting up
setup(
    name="isimport",
    version=VERSION,
    author="Ankush Bhagat (Ankush Bhagat)",
    author_email="<ankushbhagatofficial@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['rich'],
    keywords=['python', 'module', 'import', 'package', 'find'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)