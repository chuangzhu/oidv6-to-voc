from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(name='oidv6-to-voc',
      version='0.1.3',
      author='Zhu Chuang',
      author_email='genelocated@yandex.com',
      description='Convert Open Images Dataset v6 to PASCAL VOC format.',
      url='https://github.com/chuangzhu/oidv6-to-voc/',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      install_requires=['Pillow>=6.2.1'],
      entry_points={
          'console_scripts': ['oidv6-to-voc = oidv6_to_voc.__main__:main']
      })
