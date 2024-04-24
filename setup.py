from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="twelvelabs",
    version="0.1.22",
    author="Twelve Labs",
    description="SDK for Twelve Labs API",
    url="https://github.com/twelvelabs-io/twelvelabs-python",
    packages=find_packages(),
    install_requires=required,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
