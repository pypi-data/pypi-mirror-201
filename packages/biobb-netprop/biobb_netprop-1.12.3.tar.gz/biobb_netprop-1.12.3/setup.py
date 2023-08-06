import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_netprop",
    version="1.12.3",
    author="Biobb developers - Maria Paola Ferri",
    author_email="maria.ferri@bsc.es",
    description="Biobb_NetProp is use case to build a prioritize PPI Network through Disc4All pre-process database REST API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/mapoferri/Biobb_NetProp",
    project_urls={
        "Documentation": "http://biobb_netprop.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['adapters', 'docs', 'test']),
    install_requires=['biobb_common>=3.5.1','biobb_md>=3.7.1', 'biobb_analysis==3.7.0'],
    python_requires='==3.7.*',
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
