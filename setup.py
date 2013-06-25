#!/usr/bin/env python
#-*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='py-video-reupload',
    version='0.1',

    author='Damian Kęska',
    author_email='webnull.www@gmail.com',
    url='https://github.com/webnull',
    license='GNU GPLv3',

    description='Simple Python application intended to reupload videos between video hosting sites',
    long_description='Simple Python application intended to reupload videos between video hosting sites, with built-in QT4-based interface',
    keywords='youtube vimeo download streaming video save',
    
    install_requires=['you_get'],
    package_dir={'': 'src'}, 
    packages=['py_video_reupload'],
    
    entry_points = {
        'console_scripts': [
            'py_video_reupload = py_video_reupload.main:main',
        ],
    },
)
