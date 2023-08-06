from setuptools import find_packages, setup

setup(
    packages=find_packages(
        where=".",
        include=["functional_cat*"],
    ),
)
