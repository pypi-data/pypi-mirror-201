# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages


setup(
  name = "kyaah", # name of the main package (base folder i.e kyaah)
  version = "0.1.8",
  description = "Kyaah abstract away cognitive over-head of sending SMTP mail, together with other mailing operations things like, mail with file, tokens etc",
  long_description = open("README.md").read() + "\n\n" + open("CHANGELOG").read(),
  long_description_content_type="text/markdown",
  python_requires = ">=3.6",
  # platforms="any",
  
  url = "https://kyaah.readthedocs.io",
  repo = "https://github.com/usmanmusa1920/kyaah",
  author = "Usman Musa",
  author_email = "usmanmusa1920@gmail.com",
  License = "MIT",
  classifiers = [
    "Development Status :: 5 - Production/Stable",
    # "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    # "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    # "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    # "Programming Language :: Python :: 3.10",
  ],
  
  # used when people are searching for a module, keywords separated with a space
  keywords = "kyaah",
  include_package_data = True, # include files listed in MANIFEST.in
  
  # The list of packages(directories) for your library
  packages = find_packages(), # OR packages=["kyaah"] 
  # If your package is a single module, use this instead of "packages":
  # py_modules=[""] # list of files (modules) that are not in any directory (at the root dir)
  # the libraries it depends on
  
  # List of other python modules which this module depends on.  For example RPi.GPIO
  install_requires = [
    "geocoder==1.38.1",
    ]
)
