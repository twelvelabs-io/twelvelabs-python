from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="twelvelabs",
    version="0.1",
    author="Twelve Labs",
    description="SDK for Twelve Labs API",
    packages=find_packages(),
    install_requires=required,
)
