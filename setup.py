#!/usr/bin/env python
"""
Setup script for pb_video_utils. Use like this for Unix:

$ python setup.py install
"""
from distutils.core import setup
import os

setup(name='pb_video_utils',
    version='0.0.1',
    description='A tool for automating some video utilties.',
    author='Pete Bunting',
    author_email='petebunting@mac.com',
    scripts=['bin/pbv_report.py', 'bin/pbv_norm_1080.py'],
    packages=['pb_video_utils'],
    package_dir={'pb_video_utils': 'pb_video_utils'},
    license='LICENSE',
    url='https://www.github.info/petebunting/pb_video_utils',
    classifiers=['Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8'])
