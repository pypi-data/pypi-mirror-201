import setuptools
import configparser


config = configparser.ConfigParser()
config.read("setup.cfg")

# Get the values from the [metadata] section
package_name = config.get("metadata", "name")
author_name = config.get("metadata", "author")
author_email = config.get("metadata", "author_email")
description = config.get("metadata", "description")
long_description_content_type = config.get("metadata",
                                           "long_description_content_type")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=package_name,
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "dirty-tag",
    },
    author=author_name,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    packages=setuptools.find_namespace_packages(
        include=['technical_indicator.*']),
    include_package_data=True,
    package_dir={"": "src"},
    package_data={"": ["*.txt"]},
    install_requires=[
        "pandas",
        "numpy",
    ],
    tests_require=[
        'pytest',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
