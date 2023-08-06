# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:03:48 2023

@author: Petercusin
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PgsFile",
    version="0.0.6",
    author="Pan Guisheng",
    author_email="895284504@qq.com",
    description="To make file operations coding easier for literary students",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free For Educational Use",
        "Operating System :: OS Independent",
    ],
)