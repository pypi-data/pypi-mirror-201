from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'max'
LONG_DESCRIPTION = 'An intelligent virtual assistant'

# Setting up
setup(
    name="thisismaxth",
    version=VERSION,
    author="Pro-2-_grammer_Tushar",
    author_email="Tushar2010@outlook.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['AI', 'max', 'machine learning', 'assistant', 'AI Assistant'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
