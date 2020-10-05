from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(name='oidv6-to-voc',
      version='0.1',
      author='Zhu Chuang',
      author_email='genelocated@yandex.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      install_requires=['Pillow==6.2.1'])