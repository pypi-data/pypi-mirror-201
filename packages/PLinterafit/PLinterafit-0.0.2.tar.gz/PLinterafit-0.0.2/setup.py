import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PLinterafit",
    version="0.0.2",
    author="Viktor Bender, Bayarjargal N.Tugchin",
    author_email="vbender@physik.hu-berlin.de, n.bayarjargal@uni-jena.de",
    description="This is a package for Voigt fitting of a photolumiscence spectrum and statistically evaluating the fitting results.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=['PLinterafit'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'': ['example_data/ExampleData_monolayerMoS2onSi02.asc']},
    include_package_data=True,
    python_requires='>=3.6',
    keywords="PL spectra fitting",
    instal_requires=["requests>=2"],
)
