from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.4'
DESCRIPTION = 'A collection of Python utilities for developers.'

with open('requirements.txt', 'r') as requirements_file:
    REQUIREMENTS = requirements_file.read().splitlines()

with open('README.md', 'r') as readme_file:
    LONG_DESCRIPTION = readme_file.read()


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
