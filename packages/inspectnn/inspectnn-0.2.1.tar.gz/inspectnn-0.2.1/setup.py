try:
    import setuptools
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="inspectnn",
    version="0.2.1",
    description="Inference eNgine uSing aPproximate arithmEtic ComponenTs for Neural Networks",
    long_description="Inference eNgine uSing aPproximate arithmEtic ComponenTs for Neural Networks",
    url="https://github.com/SalvatoreBarone/inspect-nn",
    author="Salvatore Barone, Filippo Ferrandino",
    author_email="salvatore.barone@unina.it, fi.ferrandino@studenti.unina.it",
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.9"
    ],
    keywords="Neural Networks Approximate-Computing",
    packages=setuptools.find_packages(),#["inspectnn"],
    include_package_data=True,
    python_requires='==3.9.16',
    install_requires=["numba==0.56.4", "numpy==1.19.5", "tensorflow==2.6.4", "keras==2.6.0", "scipy==1.7.3",  "h5py==3.1.0", "protobuf<=3.20", "scikit-learn","click","tabulate"],#fare -U pymoo
    project_urls={
        "Bug Reports": "https://github.com/SalvatoreBarone/inspect-nn/issues",
        "Source": "https://github.com/SalvatoreBarone/inspect-nn",
    },
)

