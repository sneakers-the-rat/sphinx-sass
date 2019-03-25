"""
    test_sphinx_sass
    ~~~~~~~~~~~~~~~~
    Tests for :mod:`sphinx_sass.__init__` module.
"""

import os
from pathlib import Path
import sys
import unittest
import warnings

import pyfakefs
from pyfakefs.fake_filesystem_unittest import TestCase

import sphinx
from sphinx.application import Sphinx

from sphinx_sass import setup


FIXTURES = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))


class TestSetup(TestCase):

    def setUp(self):
        self.setUpPyfakefs(modules_to_reload=[
            sphinx
        ])
        packages = [
            path for path in sys.path if path.endswith('site-packages')]
        for package in packages:
            self.fs.add_real_directory(package)
        self.fs.add_real_directory(FIXTURES)

    def test_setup(self):

        docs = Path(os.path.join(os.path.dirname(__file__), 'docs'))

        srcdir = docs / 'source'
        builddir = docs / 'build'
        doctreedir = builddir / '.doctrees'

        with open(os.path.join(FIXTURES, 'conf.py'), 'r') as file_in:
            conf = file_in.read()
        self.fs.create_file(str(srcdir / 'conf.py'), contents=conf)
        # self.fs.create_dir(srcdir)
        app = Sphinx(srcdir, None, builddir, doctreedir, 'html')
        setup(app)

        config = app.config

        print(config.values)
        self.assertTrue(os.path.exists(builddir))
        self.assertTrue(os.path.exists(doctreedir))

        self.assertIn('sass_configs', config)
        self.assertDictEqual(config.sass_configs, {})
