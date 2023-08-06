from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Basic 2 point crossover and mutation'
LONG_DESCRIPTION = 'A basic 2 point crossover and mutation package using dict.'

# Setting up
setup(
    name="crossnmut",
    version=VERSION,
    author="Bishal Bhandari",
    author_email="<bishalbhaandari62@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['random', 'numpy'],
    keywords=['python', 'genetic algorithm', 'crossover', 'mutation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)