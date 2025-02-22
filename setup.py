from setuptools import setup, find_packages

with open("README.md", 'r', encoding="utf-8") as f:
  description = f.read()

setup(
  name="easshy",
  version="0.0.1",
  author="Fastiraz",
  author_email="",
  description="A simple tool that lets you easily manage your SSH servers credentials.",
  long_description=description,
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
      "easshy = easshy.easshy:main",
    ],
  },
)
