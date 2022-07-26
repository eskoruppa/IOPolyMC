from setuptools import setup

setup(name='iopolymc',
      version='0.0.2',
      description='A module to read and write PolyMC input and output files',
      url='https://github.com/esasen/IOPolyMC',
      author='Enrico Skoruppa',
      author_email='enrico.skoruppa@gmail.com',
      license='MIT',
      packages=['iopolymc'],
      package_dir={
            'iopolymc': 'iopolymc',
      },
      include_package_data=True,
      package_data={'': ['database/*']},
      install_requires=[
          'numpy<=1.22',
      ],
      zip_safe=False) 
