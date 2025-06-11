#!/usr/bin/env python
"""
Setup script for The Elidoras Codex testing framework.
"""
import os
import sys
from setuptools import setup, find_packages

# Get the directory of this file
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Read the README file
with open(os.path.join(ROOT_DIR, "tests", "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

# Define package requirements
REQUIREMENTS = [
    "pytest>=7.0.0",
    "pytest-cov>=4.1.0", 
    "pytest-mock>=3.10.0",
    "python-dotenv>=1.0.0",rr
    "requests>=2.28.0",
    "python-wordpress-xmlrpc>=2.3.0",
]

DEV_REQUIREMENTS = [
    "black>=23.3.0",
    "flake8>=6.0.0",
    "mypy>=1.3.0",
    "isort>=5.12.0",
    "pre-commit>=3.3.2",
]

setup(
    name="tec-testing",
    version="1.0.0",
    description="Testing framework for The Elidoras Codex",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Polkin Rishall",
    author_email="architect@elidorascodex.com",
    url="https://github.com/yourusername/astradigital-engine",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": REQUIREMENTS + DEV_REQUIREMENTS,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
