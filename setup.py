from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy 8tracks',
    version=get_version('mopidy_eight_tracks/__init__.py'),
    url='https://github.com/dz0ny/mopidy 8tracks',
    license='Apache License, Version 2.0',
    author='dz0ny',
    author_email='dz0ny@ubuntu.si',
    description='Mopidy extension for  8tracks.com',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 0.18',
        'Pykka >= 1.1',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'flake8',
        'httpretty',
        'mock >= 1.0',
    ],
    entry_points={
        'mopidy.ext': [
            'eight_tracks = mopidy_eight_tracks:EightTracksExtension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)