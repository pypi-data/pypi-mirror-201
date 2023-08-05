from setuptools import setup, find_packages
import os
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="pandas_gbq_magic",
    version="1.1.1",
    author="Pulak JS",
    author_email="pulaksachdeva@gmail.com",
    description="The package provides as magic on top of Pandas GBQ to make querying in Jupter envioronment easy and user  friendly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PulakSachdeva52/Big-Query-Magic/",
    project_urls={
        "Bug Tracker": "https://github.com/PulakSachdeva52/Big-Query-Magic/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        # List your package dependencies here
    ],
)
