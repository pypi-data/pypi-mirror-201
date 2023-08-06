import os

from setuptools import find_packages, setup

VERSION = '0.0.1'
DESCRIPTION = 'A 2D mining game made with pygame.'
LONG_DESCRIPTION = 'A 2D mining game made with pygame, where you control a drill on an infinite map with farious biomes both at surfacce level and in caves.'

# Setting up
setup(
    name="terrario",
    version=VERSION,
    author="MaitreRenard18, Wagister",
    author_email="<maitre.renardowo@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame', 'opensimplex'],
    keywords=['python', 'game', '2d', 'pygame'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)