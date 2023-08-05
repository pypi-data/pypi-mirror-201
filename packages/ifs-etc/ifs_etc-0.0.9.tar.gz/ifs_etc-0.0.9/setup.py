import pdb

from setuptools import setup, find_packages
import re

package = "ifs_etc"

with open("README.md", "r") as fh:
    long_description = fh.read()


def find_version(package):
    version_file = open("src/" + package + "/__init__.py").read()
    rex = r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format('__version__')
    return re.search(rex, version_file).group(1)

setup(
    name=package,
    version=find_version(package),
    description='exposure time calculator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='linlin',
    author_email='linlin@shao.ac.cn',
    packages=find_packages(where="src"),
    install_requires=['pandas==1.3.3',
                      'numpy==1.20.2',
                      'h5py==2.8.0',
                      'einops==0.3.2',
                      'matplotlib==3.0.2',
                      'astropy==4.2.1',
                      'scipy==1.1.0',
                      'extinction==0.4.0',
                      'commentjson==0.9.0'],
    package_dir={"": "src"},
    include_package_data=True,
    # exclude_package_data={"": ["README.md"]},
    python_requires='>=3',
)

