#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, setuptools

__author__ = 'Iván de Paz Centeno'


setup(name='vrpwrp',
      version='0.1',
      description='Vision-algorithms Requests Processing Wrappers for deep-learning Computer Vision algorithms on the cloud.',
      url='http://github.com/ipazc/vrpwrp',
      author='Iván de Paz Centeno',
      author_email='ipazc@unileon.es',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'requests',
          'pillow'
      ],
      zip_safe=False)