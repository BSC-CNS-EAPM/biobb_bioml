"""
Setup module for standard Pypi installation.
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_bioml",
    version="0.1",

    author="Biobb developers",
    author_email="acanella@bsc.es",
    description="BioBB_bioml performs feature detection and extraction to train ML algorithms to detect protein similarities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/BSC-CNS-EAPM/biobb_bioml",
    project_urls={
        "Documentation": "...",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test']),
    include_package_data=True,
    install_requires=['psutil', 'numpy', 'biopython==1.79'],
    python_requires='>=3.7',
    extras_require={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Linux :: Ubuntu",
    ],
)
