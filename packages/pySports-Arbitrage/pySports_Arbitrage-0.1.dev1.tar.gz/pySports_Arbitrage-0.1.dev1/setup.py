from setuptools import setup, find_packages

setup(
    name='pySports_Arbitrage',
    version='0.1dev1',
    author='Phil Rongo',
    packages=find_packages(),
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    python_requires='>=3.6'
)