from setuptools import setup, find_packages
from pathlib import Path
import os

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
version_file = os.path.join(os.path.dirname(__file__), "VERSION")
with open(version_file, "r") as f:
    version = f.read().strip()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="twelvelabs",
    version=version,
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
