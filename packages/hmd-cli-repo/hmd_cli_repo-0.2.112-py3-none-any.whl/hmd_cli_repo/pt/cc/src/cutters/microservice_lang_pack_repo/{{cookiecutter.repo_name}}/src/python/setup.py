from setuptools import setup, find_packages
import pathlib

repo_dir = pathlib.Path(__file__).absolute().parent.parent.parent
version_file = repo_dir / "meta-data" / "VERSION"

with open(version_file, "r") as vfl:
    version = vfl.read().strip()

setup(
    name="{{ cookiecutter.repo_name }}",
    version=version,
    description="{{ cookiecutter.description }}",
    author="{{ cookiecutter._author }}",
    author_email="{{ cookiecutter._author_email }}",
    license="unlicensed",
    package_data={"{{ cookiecutter.__lang_module_name }}": ["schemas/**/*.hms"]},
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
