from setuptools import setup, find_packages
from tph_lang import __version__


readme = open("README.md", "r").read()

requirements = ["arpeggio", "click", "pysimplegui"]

setup(
    author="Eduardo Maschio",
    python_requires=">=3.8",
    description="tph programming language: an APL+Befunge inspired 2d array language.",
    long_description=readme,
    include_package_data=True,
    name="tph",
    packages=find_packages(include=["tph", "tph.*"]),
    requires=requirements,
    version=__version__
)
