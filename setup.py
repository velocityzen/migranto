import os
from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

install_requires = []
try:
    import argparse
except ImportError:
    install_requires.append('argparse')

setup(
    name='migranto',
    version='0.1.10',
    author='Alexey Novikov',
    author_email='velocityzen@gmail.com',
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'PostgreSQL': ["psycopg2"],
        },
    url='https://github.com/velocityzen/migranto',
    license='BSD',
    description='Simple SQL migration tool for SQLite and PostgreSQL',
    long_description = read('README.md'),
    zip_safe=False,
    entry_points="""
    [console_scripts]
    migranto = migranto:main
    """
)
