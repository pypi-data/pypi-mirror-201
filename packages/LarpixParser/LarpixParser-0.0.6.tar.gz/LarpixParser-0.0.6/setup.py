#!/usr/bin/env python

import setuptools

VER = "0.0.6"

setuptools.setup(
    name="LarpixParser",
    version=VER,
    author="Yifan C. and others",
    author_email="cyifan@slac.stanford.edu",
    description="A package parsing the larpix output to hit-level",
    url="https://github.com/YifanC/larpix_readout_parser",
    packages=setuptools.find_packages(where="src"), #"where" is needed; "include=['LarpixParser']" is not necessary 
    package_dir={"":"src"},
    package_data={"LarpixParser": ["config_repo/*.yaml",
                                   "config_repo/dict_repo/*.pkl"]},
    install_requires=["numpy", "h5py", "fire"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    python_requires='>=3.2',
)
