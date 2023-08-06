'''setup config for pypi'''
from setuptools import setup, find_packages

with open("lementpro/readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lementpro",
    version="0.1.7",
    author="Author",
    author_email="your_email@example.com",
    description="Description of package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/your_package_name",
    packages=find_packages(exclude=["src", "tests", "update_checker"]),
    install_requires=[
        "requests>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
