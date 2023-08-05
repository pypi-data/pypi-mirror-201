import os
from setuptools import find_packages, setup


NAME = 'inkscape_layer_utils'
VERSION = '0.0.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=NAME,
    version=VERSION,
    author="Torsten Wylegala",
    author_email="mail@twyleg.de",
    description=("SImple library to extract and manipulate layers from inscape SVGs"),
    license="GPL 3.0",
    keywords="inkscape svg layer utilities",
    url="https://github.com/twyleg",
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=[],
    cmdclass={}
)
