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
    install_requires=[
        "numba>=0.45.1",
        "numpy>=1.16.4",
        "pandas>=0.25.0",
        "pyts==0.8.0",
        "scikit-learn>=0.21.2",
        "statsmodels>=0.10.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
