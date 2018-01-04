"""setup module"""
from setuptools import setup, find_packages

setup(name='cryptowatch',
      version='0.1',
      description='cryptowat.ch cryptocurrency Exchange API Pyhon Client',
      url='http://github.com/xmatthias/cryptowatch',
      author='Matthias Voppichler',
      author_email='xmatthias@outlook.com',
      license='GPL3',
      packages=find_packages(),
      install_requires=[
          'requests'
      ],
      zip_safe=False)
