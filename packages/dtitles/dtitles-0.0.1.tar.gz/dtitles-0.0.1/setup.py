from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Title package that I made for fun lol'

# Setting up
setup(
    name="dtitles",
    version=VERSION,
    author="006",
    author_email="doggydurgin54@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['ctypes'],
    keywords=['python', 'title', 'window titles', 'window'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)