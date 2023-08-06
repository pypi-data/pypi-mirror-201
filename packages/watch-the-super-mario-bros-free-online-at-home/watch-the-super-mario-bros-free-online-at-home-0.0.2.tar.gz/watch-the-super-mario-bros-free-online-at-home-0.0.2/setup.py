from setuptools import setup
import setuptools

# with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
    
    version='0.0.2',
    description= 'Watch "The Super Mario Bros. Movie" Free Online At Home',
    name="watch-the-super-mario-bros-free-online-at-home",
    author="john",
    author_email="john@gmail.com",
    # long_description=long_description,
    long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
    install_requires=[],
    keywords=['The super mario bros'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)