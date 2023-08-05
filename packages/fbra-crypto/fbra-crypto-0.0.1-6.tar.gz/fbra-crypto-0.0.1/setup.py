from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'cipher and decipher values'

setup(
    name="fbra-crypto",
    version=VERSION,
    author="Felix Brändli",
    author_email="",
    description=DESCRIPTION,
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=["cryptography"],

    keywords=['python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)