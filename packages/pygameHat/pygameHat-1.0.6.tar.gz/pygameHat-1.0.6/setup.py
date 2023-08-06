from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.6'
DESCRIPTION = 'Pygame game-making engine'

# Setting up
setup(
    name="pygameHat",
    version=VERSION,
    author="Wojciech Błajda",
    author_email="<mail@mail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'engine', 'pygame'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
