from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Watch "The Super Mario Bros. Movie" Free Online At Home'


# Setting up
setup(
    name="watch-the-super-mario-bros-free-online-at-home",
    version=VERSION,
    author="john",
    author_email="john@gmail.com",
    long_description_content_type="text/markdown",
    long_description= "file: README.md",
    packages=find_packages(),
    install_requires=[],
    keywords=['The super mario bros'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)