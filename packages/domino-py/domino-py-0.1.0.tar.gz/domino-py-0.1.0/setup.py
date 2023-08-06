from setuptools import setup, find_packages
from distutils.util import convert_path
from codecs import open
import os


package_name = "domino"

# Get version from version.py
version_dict = {}
ver_path = convert_path(f'{package_name}/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), version_dict)

# Get the long description from the README file
path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(path, "README.md")) as f:
    long_description = f.read()

# Requirements
with open(os.path.join(path, "requirements.txt")) as f:
    install_requires = f.read().strip().split("\n")

# Extra requirements - airflow
with open(os.path.join(path, "requirements-airflow.txt")) as f:
    install_extra_requires = f.read().strip().split("\n")


setup(
    name=f"{package_name}-py",
    version=version_dict['__version__'],
    description="Domino project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Luiz Tauffer and Vinicius Vaz",
    author_email="luiz@taufferconsulting.com",
    keywords=["airflow", "UI"],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={
        "airflow": install_extra_requires,
    },
    entry_points={
        "console_scripts": [
            "domino = domino.cli.cli:cli",
        ],
    },
)