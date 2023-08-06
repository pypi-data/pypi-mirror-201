#!python


import setuptools
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('VAE_G2P/vae_g2p.py').read(),
    re.M).group(1)



with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(
    name="VAE_G2P",
    version=version,
    author="David Blair",
    author_email="david.blair@ucsf.edu",
    description="A fully generative probability model that maps gene-based knowledge directly to disease symptoms, including their reported frequencies.",
    long_description_content_type="text/markdown",
    url="https://github.com/daverblair/VAE_G2P",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'torch',
        'pyro-ppl',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
