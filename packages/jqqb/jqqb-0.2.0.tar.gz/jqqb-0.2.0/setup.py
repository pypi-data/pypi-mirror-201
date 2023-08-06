import setuptools
import unittest


def unittest_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jqqb",
    version="0.2.0",
    author="Connecting Food",
    author_email="developers@connecting-food.com",
    description="Python parsing, evaluation and inspection tools "
    "for jQuery-QueryBuilder rules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Connecting-Food/jQueryQueryBuilder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires=">=3.6",
    test_suite="setup.unittest_test_suite",
)
