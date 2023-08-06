import sys, os
from setuptools import setup, find_packages
import subprocess

NAME = "kofi"
HERE = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join(HERE, NAME, "_version.py")) as f:
    exec(f.read(), {}, version_ns)

with open(os.path.join(HERE, "requirements.txt")) as f:
    reqs = f.read().strip().split("\n")

setup(
    name=NAME,
    version=version_ns["__version__"],
    description="Color scales and color conversion made easy for Python.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Education'
    ],
    keywords="color colors colorspace scale spectrum",
    author="Francis Selorm Kponyo",
    author_email="pojoba01@gmail.com",
    url="http://github.com/Sweelol/spectra",
    license="MIT",
    packages=find_packages(exclude=["test",]),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=reqs,
    tests_require=[],
    test_suite="test"
)
