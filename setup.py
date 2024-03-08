from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="airfoilreader",
    version="1.0",
    author="Han Zexu",
    author_email="sin390@foxmail.com",
    description="A module to read an airfoil datafile and parse the result as a dict.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sin390/airfoilreader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)