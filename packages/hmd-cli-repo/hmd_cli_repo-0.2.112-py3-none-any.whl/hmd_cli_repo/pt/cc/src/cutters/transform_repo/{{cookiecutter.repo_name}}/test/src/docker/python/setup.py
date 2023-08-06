import pathlib

from setuptools import find_packages, setup

setup(
    name="module_name",
    version="0.0.1",
    description="{{ cookiecutter.description }}",
    author="{{ cookiecutter._author }}",
    author_email="{{ cookiecutter._author_email }}",
    license="unlicensed",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
