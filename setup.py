import os
import re

from pkg_resources import DistributionNotFound, get_distribution
from setuptools import find_packages, setup

INSTALL_REQUIRES = ["numpy>=1.24.4", "scipy>=1.10.0", "scikit-image>=0.21.0", "PyYAML", "typing-extensions>=4.9.0", "scikit-learn>=1.3.2"]

# If none of packages in first installed, install second package
CHOOSE_INSTALL_REQUIRES = [
    (
        ("opencv-python>=4.9.0", "opencv-contrib-python>=4.9.0", "opencv-contrib-python-headless>=4.9.0"),
        "opencv-python-headless>=4.9.0",
    )
]


def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(current_dir, "albumentations", "__init__.py")
    with open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        return f.read()


def choose_requirement(mains, secondary):
    """If some version of main requirement installed, return main,
    else return secondary.

    """
    chosen = secondary
    for main in mains:
        try:
            name = re.split(r"[!<>=]", main)[0]
            get_distribution(name)
            chosen = main
            break
        except DistributionNotFound:
            pass

    return str(chosen)


def get_install_requirements(install_requires, choose_install_requires):
    for mains, secondary in choose_install_requires:
        install_requires.append(choose_requirement(mains, secondary))

    return install_requires


setup(
    name="albumentations",
    version=get_version(),
    description="Fast image augmentation library and easy to use wrapper around other libraries",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Vladimir I. Iglovikov, Mikhail Druzhinin, Alex Parinov, Alexander Buslaev, Eugene Khvedchenya",
    license="MIT",
    url="https://github.com/albumentations-team/albumentations",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    install_requires=get_install_requirements(INSTALL_REQUIRES, CHOOSE_INSTALL_REQUIRES),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
