from os import path
import analytics_utils
import setuptools


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="analytics_utils",
    version=analytics_utils.__version__,
    author="Patrick Silva Ferraz, Leandro Souza de Oliveira",
    author_email="patrick.ferraz@outlook.com",
    description="Package with functions for data analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patricksferraz/analytics-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
