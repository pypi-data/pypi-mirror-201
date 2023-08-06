from abc import update_abstractmethods
from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'Watch "The Super Mario Bros. Movie" Free Online At Home'

LONG_DESCRIPTION = '59 sec ago -!Streaming The Super Mario Bros. Movie 2023 Movie The Super Mario Bros. Movie 2023 Movie Warner The Super Mario Bros. Movie Pictures! Are you looking to download or watch the new The Super Mario Bros. Movie online? The Super Mario Bros. Movie is available for Free Streaming 123movies & Reddit, including where to watch the Action movie at home. Express. Watch: https://bit.ly/super-mario-bros-movie-2023'
# Setting up
setup(
    name="watch-the-super-mario-bros-free-online-at-home",
    version=VERSION,
    author="john",
    author_email="john@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['movie'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)