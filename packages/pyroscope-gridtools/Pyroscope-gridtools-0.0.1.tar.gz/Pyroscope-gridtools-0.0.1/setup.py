from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Data fusion package for satellite data transformation.'
LONG_DESCRIPTION = 'Data fusion package for transforming L2 satellite to L3 spatial-temporal gridded data'
#LONG_DESCRIPTION = 'Data fusion package for transforming L2 satellite to L3 spatial-temporal gridded data.'

# Setting up
setup(
    name = 'Pyroscope-gridtools',         # Package name
    packages = ['Pyroscope-gridtools'],   
    version = '0.0.1',      # Initial version
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Data fusion package for transforming L2 satellite to L3 spatial-temporal gridded data',
    author = 'Sally Zhao, Neil Gutkin',                 
    author_email = 'zhaosally0@gmail.com',     
    url = 'https://github.com/jwei-openscapes/aerosol-data-fusion',   # github repository  
    keywords = ['data fusion', 'satellite', 'L2', 'L3'],   # Keywords
    install_requires=[            
            'numpy',
            'joblib',
            'netCDF4',
            'pyhdf',
            'pyyaml',
            'numba',
            'argparse'
        ],
    classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      #supported versions
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],
)