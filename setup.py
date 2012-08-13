import codecs
from distutils.core import setup
import os
from setuptools import find_packages

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='migranto',
    version='0.1.0',
    author='Alexey Novikov',
    author_email='velocityzen@gmail.com',
    packages=find_packages(),
    url='https://github.com/velocityzen/migranto',
    license='BSD licence, see LICENCE.txt',
    description='Simple SQL migration tool for SQLite and PostgreSQL',
    long_description = read('README.md'),
    zip_safe=False,
    entry_points="""
    [console_scripts]
    migranto = migranto:main
    """
)