from setuptools import setup, find_packages

from setuptools_scm import get_version
import os

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


def get_version():
    version = "0.1.25"
    local_version = os.environ.get("SCM_REV")
    if local_version:
        version += "+" + local_version
    return version


setup(
    version=get_version(),
    packages=find_packages(),
    install_requires=requirements,
    package_data={
        "": ["*.yaml"],
    },
    include_package_data=True,
)
