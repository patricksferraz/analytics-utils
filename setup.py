import setuptools

from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="analytics_utils",
    version="0.1.dev",
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
