from setuptools import setup, find_packages

setup(
    name="luau",
    version="0.1.1",
    author="nightcycle",
    author_email="coyer@nightcycle.us",
    description="a basic python package for writing luau scripts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=["re", "typing"],
)