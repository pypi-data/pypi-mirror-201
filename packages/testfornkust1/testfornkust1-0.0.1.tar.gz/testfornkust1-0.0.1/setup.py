from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="testfornkust1", # Replace with your own username
    version="0.0.1",
    author="timenet2300",
    author_email="timenet2300@gmail.com",
    description="A small package to work with prime numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clement-bonnet/medium-first-package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)