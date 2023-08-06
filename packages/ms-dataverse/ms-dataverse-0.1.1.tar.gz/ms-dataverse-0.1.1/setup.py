from setuptools import setup, find_packages

setup(
    name="ms-dataverse",
    version="0.1.1",
    description="DataverseORM is a Python module that simplifies working with Microsoft Dataverse by providing a lightweight Object-Relational Mapper (ORM) for querying, creating, updating, and deleting entities. It uses the Dataverse Web API for communication and includes optional metadata validation to ensure that entities and properties exist in the connected Dataverse environment.",
    author="Denniz Svens",
    author_email="denniz@liminsity.se",
    url="https://github.com/DennizSvens/ms-dataverse",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "requests",
    ],
)
