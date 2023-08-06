from setuptools import setup, find_packages

setup(
    name="midas-data-util",
    version="0.1.0",
    author="nightcycle",
    author_email="coyer@nightcycle.us",
    description="a package with useful functions for downloading and working with midas generated analytics data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=["adal", "azure-kusto-data", "pandas"],
)