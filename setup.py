#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(name='qextractor',
      version='1.0.0',
      author='Rafael Reis',
      author_email='rafael2reis@gmail.com',
      url='http://www.my_program.org',
      download_url='http://www.my_program.org/files/',
      description='Quotation Extractor for Portugues',
      long_description='Several modules to construct and test a machine learning model to solve the task of Quotation Extraction',

      packages = find_packages(),
      include_package_data = True,
      package_data = {
        '': ['*.txt', '*.rst'],
        'my_program': ['data/*.html', 'data/*.css'],
      },
      exclude_package_data = { '': ['README.txt'] },
      
      scripts = ['bin/qextractor'],
      
      keywords='python tools utils qextractor machine learning quotation',
      license='GPL',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Topic :: Internet',
                   'Topic :: Internet :: WWW/HTTP',
                  ],
                  
      #setup_requires = ['python-stdeb', 'fakeroot', 'python-all'],
      install_requires = ['setuptools', 'numpy','sklearn'],
     )
