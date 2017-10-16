#!/usr/bin/env python3

from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

__version__ = "0.1.1"

requirements = [
    "requests >= 2.10.0",
    "appdirs >= 1.4.3"
]

setup(
    name="cryptoquote",
    version=__version__,
    description="Cryptocurrency quotes on the command line",
    long_description=readme + "\n\n" + history,
    author="Sean Leavey",
    author_email="cryptoquote@attackllama.com",
    url="https://github.com/SeanDS/cryptoquote",
    packages=[
        "cryptoquote"
    ],
    package_dir={
        "cryptoquote": "cryptoquote"
    },
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'cq = cryptoquote.__main__:main'
        ]
    },
    license="GPLv3",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Envionment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
