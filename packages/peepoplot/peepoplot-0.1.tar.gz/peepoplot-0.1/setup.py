from setuptools import setup, find_packages


setup(
    name='peepoplot',
    version='0.1',
    license='MIT',
    author="Ramon Murilo",
    author_email='ramonmurilo@id.uff.br',
    packages=find_packages('peepoplot'),
    package_dir={'': 'peepoplot'},
    url='https://github.com/Ramonmurilo/peepoplot',
    keywords='peepoplot',
    install_requires=[
          'numpy',
          'matplotlib',
          'cartopy',
      ],

)