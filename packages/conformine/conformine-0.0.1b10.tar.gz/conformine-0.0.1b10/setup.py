import os.path

from setuptools import setup, find_packages
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent


with open(os.path.join(os.path.abspath(get_project_root()), "conformine/README.md"), "r") as fh:
    long_description = fh.read()


setup(
    name='conformine',
    version='0.0.1b10',
    description='ConforMine, a predictor of conformational variability from amino acid sequence',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="b2bTools,biology,bioinformatics,bio-informatics,fasta,proteins,protein-conformation,"
             "conformational-variability",
    # url='https://github.com/your-username/your-package-name',
    author='Jose Gavalda-Garcia',
    author_email='jose.gavalda.garcia@vub.be',
    maintainer="Jose Gavalda-Garcia, Adrian Diaz, Wim Vranken",
    maintainer_email="jose.gavalda.garcia@vub.be, adrian.diaz@vub.be, wim.vranken@vub.be",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6, <3.10",

    install_requires=[
        "joblib", #CVE-2022-21797
        "networkx",
        "pomegranate",
        "numpy", #CVE-2021-41496, CVE-2021-34141, CVE-2021-41495
        "Pillow",
        "PyYAML",
        "scikit-learn>=1.0.1",
        "scipy",
        "six",
        "threadpoolctl",
        "torch>=1.8.0",
        "torchvision",
        "pandas",
        "requests",
        "biopython"

    ],
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
    ],
)
