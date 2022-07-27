from setuptools import setup

setup(name='iopolymc',
      version='0.0.2',
      description='A module to read and write PolyMC input and output files',
      url='https://github.com/esasen/IOPolyMC',
      author='Enrico Skoruppa',
      author_email='enrico.skoruppa@gmail.com',
      license='MIT',
      packages=['iopolymc'],
      install_requires=[
          'numpy',
      ],
      zip_safe=False)
