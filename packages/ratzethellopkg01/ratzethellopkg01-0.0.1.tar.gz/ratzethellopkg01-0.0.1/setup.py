from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'This package prints your name and asks question.'

# Setting up
setup(
    name="ratzethellopkg01",
    version=VERSION,
    author="Abhishek Raturi (ratzet)",
    author_email="abhishek.raturi6@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[''],
    keywords=['hello'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)