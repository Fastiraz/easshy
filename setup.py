# from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
  name="easshy",
  version="0.1.0",
  author="Fastiraz",
  author_email="",
  description="A simple tool that lets you easily manage your SSH servers credentials.",
  long_description_content_type="text/markdown",
  url="https://github.com/Fastiraz/easshy",
  packages=find_packages(where="src"),
  package_dir={"": "src"},
  install_requires=[
    "keyboard",
    "cryptography"
  ],
  include_package_data=True,
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.10",
  entry_points = {
    "console_scripts": [
      # "easshy = easshy:easshy"
      "easshy = easshy.easshy:main"
    ],
  },
)
