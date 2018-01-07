"""setup module"""
from setuptools import setup, find_packages

from cryptowatch.version import __version__

setup(name="cryptowatch",
      version=__version__,
      description="cryptowat.ch cryptocurrency Exchange API Pyhon Client",
      url="http://github.com/xmatthias/cryptowatch",
      author="Matthias Voppichler",
      author_email="xmatthias@outlook.com",
      license="Apache License 2.0",
      scripts=["cryptowat.py"],
      python_requires='>=3',
      packages=find_packages(),
      install_requires=[
          "requests>=2",
          "colorama",
          "pandas>=0.21"
      ],
      zip_safe=False)
