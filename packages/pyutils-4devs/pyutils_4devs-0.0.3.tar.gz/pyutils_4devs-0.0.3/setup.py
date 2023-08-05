from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.3'
DESCRIPTION = 'A collection of Python utilities for developers.'
LONG_DESCRIPTION = 'A collection of Python utilities for developers.'

with open('requirements.txt', 'r') as requirements_file:
    REQUIREMENTS = requirements_file.read().splitlines()


setup(
    name="pyutils_4devs",
    version=VERSION,
    author="Beker-Dev",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/Beker-Dev/pyutils4devs",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    keywords=['python', 'utils', 'jwt', 'minio', 'encrypt', 'file', 'secret', 'key'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
