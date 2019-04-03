"""
    Setup.py
    ~~~~~~~~
"""
import os
import re

from setuptools import setup, find_packages

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


def read(*paths, **kwargs):
    with open(os.path.join(*paths), 'r', **kwargs) as file_in:
        return file_in.read()


def find_version(*file_paths):
    version_file = read(PACKAGE_DIR, '__init__.py')
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


PACKAGE_DIR = os.path.join(PROJECT_ROOT, 'sphinxcontrib', 'sass')

DISTNAME = 'sphinxcontrib-sass'
DESCRIPTION = 'Compile SASS and SCSS to CSS for Sphinx HTML documentation'
LONG_DESCRIPTION = read(PROJECT_ROOT, 'README.rst')
AUTHOR = 'Mark Wibrow'
AUTHOR_EMAIL = None
URL = 'https://github.com/mwibrow/sphinx-sass'
LICENSE = 'MIT'


REQUIREMENTS = read(PROJECT_ROOT, 'requirements.txt')
REQUIREMENTS_DEV = read(PROJECT_ROOT, 'requirements-dev.txt')


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Documentation',
    'Topic :: Documentation :: Sphinx',
    'Topic :: Utilities',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
]

setup(
    name=DISTNAME,
    version=find_version(PACKAGE_DIR, '__init__.py'),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    license=LICENSE,
    platforms='any',
    packages=find_packages(
        where=PROJECT_ROOT,
        exclude=['tests', 'docs']
    ),
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    extras_require={
        'dev': REQUIREMENTS_DEV
    },
    python_requires='>=3.5',
    namespace_packages=['sphinxcontrib'],
    zip_safe=False,
)
