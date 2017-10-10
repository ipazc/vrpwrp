#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, setuptools

__author__ = 'Iván de Paz Centeno'

def readme():
    with open('README.rst', encoding="UTF-8") as f:
        return f.read()

if sys.version_info < (3, 4, 1):
    sys.exit('Python < 3.4.1 is not supported!')

setup(name='vrpwrp',
      version='0.0.7',
      description='Vision-algorithms Requests Processing Wrappers for deep-learning Computer Vision algorithms on the cloud.',
      long_description=readme(),
      url='http://github.com/ipazc/vrpwrp',
      author='Iván de Paz Centeno',
      author_email='ipazc@unileon.es',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'requests',
          'pillow'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      keywords="vrpwrp face_detection face_recognition face deep-learning computer vision face detection face recognition api rest wrapper",
      zip_safe=False)
