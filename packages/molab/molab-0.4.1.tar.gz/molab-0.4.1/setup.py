"""Setup for the chocobo package."""

from setuptools import setup, find_packages


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    author="Sean Jabro",
    author_email="sean.jabro@outlook.com",
    name='molab',
    license="MIT",
    description='molab is a python package for configuring Morpheus training lab environments.',
    version='0.4.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/morpheus_training/molab',
    packages=find_packages() + find_packages(where='template_files'),
    package_dir={'template_files': 'template_files'},
    package_data={'molab': ['template_files/*.*']},
    python_requires=">=3.8",
    install_requires=["urllib3","requests","requests_futures","loguru","morpheus-cypher","importlib_resources"],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
)