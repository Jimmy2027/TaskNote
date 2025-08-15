#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()


requirements = ["Click>=7.0", "tomli; python_version < '3.11'"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Hendrik Klug",
    author_email="hendrik.klug@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Convert GitHub notifications to taskwarrior tasks",
    entry_points={
        "console_scripts": ["tasknote=tasknote.cli:main"],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="tasknote",
    name="tasknote",
    packages=find_packages(include=["tasknote", "tasknote.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Jimmy2027/tasknote",
    version="0.1.0",
    zip_safe=False,
)
