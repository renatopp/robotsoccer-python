# -*- coding:utf-8 -*-
# Copyright (C) 2011 Renato de Pontes Pereira, renato.ppontes at gmail dot com
#
# This module is part of robotsoccer-python and is released under 
# the MIT  License: http://www.opensource.org/licenses/mit-license.php
try:
    from setuptools import setup
except ImportError as e:
    from distutils.core import setup

long_description = '''
    Python library for robotsoccer match simulator communication.
'''

setup(
    name='RobotSoccer',
    version='0.1',
    url='http://inf.ufrgs.br/~rppereira/robotsoccer.html',
    download_url='https://github.com/renatopp/robotsoccer-python',
    license='MIT License',
    author='Renato de Pontes Pereira',
    author_email='renato.ppontes@gmail.com',
    description='Python library for robotsoccer match simulator communication.',
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='simulation robotics artificial intelligence',
    packages=[
        'robotsoccer',
    ],
)