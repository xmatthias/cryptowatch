"""setup module"""
from setuptools import setup, find_packages

setup(name="cryptowatch",
      version="0.1",
      description="cryptowat.ch cryptocurrency Exchange API Pyhon Client",
      url="http://github.com/xmatthias/cryptowatch",
      author="Matthias Voppichler",
      author_email="xmatthias@outlook.com",
      license="Apache License 2.0",
      scripts=["cryptowat.py"],
      python_requires='>=3',
      packages=find_packages(),
      install_requires=[
          "requests",
          "colorama",
          "pandas"
      ],
      zip_safe=False)
