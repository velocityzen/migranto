import os
from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='migranto',
    version='0.1.9',
    author='Alexey Novikov',
    author_email='velocityzen@gmail.com',
    packages=find_packages(),
    install_requires = ["psycopg2"],
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
