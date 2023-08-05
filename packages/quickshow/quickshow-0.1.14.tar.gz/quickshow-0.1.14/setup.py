import re

from setuptools import find_packages
from setuptools import setup


def get_version():
    filename = "quickshow/__init__.py"
    with open(filename) as f:
        match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M)
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_long_description():
    with open("README.md") as f:
        long_description = f.read()
        return long_description


version = get_version()


setup(
    name="quickshow",
    version="0.1.14",
    author="parkminwoo",
    author_email="parkminwoo1991@gmail.com",
    description="Quick-Show provides simply but powerful insight plots",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/DSDanielPark/quick-show",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["seaborn", "numpy", "pandas", "matplotlib", "scikit-learn"],
    keywords="Visuallization, Matplotlib, Plotting, Data Science",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
