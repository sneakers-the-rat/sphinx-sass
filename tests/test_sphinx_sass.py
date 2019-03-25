"""
    test_sphinx_sass
    ~~~~~~~~~~~~~~~~
    Tests for :mod:`sphinx_sass.__init__` module.
"""

import logging
import os
from pathlib import Path
import sys
import unittest
import warnings

from docutils.parsers.rst import directives
from docutils.parsers.rst import roles
import pyfakefs
from pyfakefs.fake_filesystem_unittest import TestCase

import sphinx
from sphinx.application import Sphinx

from sphinx_sass import setup

FIXTURES = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))


def disable_sphinx_loggers():
    """Disable the loggers from sphing."""
    for name in logging.root.manager.loggerDict:
        if name.startswith('sphinx'):
            logger = logging.getLogger(name)
            logger.disabled = True


def clear_docutils_cache():
    """Clear docutils cache for directives and roles."""
    directives._directives = {}
    roles._roles = {}


class TestSetup(TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        packages = [
            path for path in sys.path if path.endswith('site-packages')]
        for package in packages:
            self.fs.add_real_directory(package)
        self.fs.add_real_directory(FIXTURES)
        clear_docutils_cache()
        disable_sphinx_loggers()

    def test_setup(self):
        """Extension setup adds extension options."""
        docs = Path(os.path.join(os.path.dirname(__file__), 'docs'))

        srcdir = docs / 'source'
        builddir = docs / 'build'
        doctreedir = builddir / '.doctrees'
        self.fs.create_dir(srcdir)

        app = Sphinx(srcdir, None, builddir, doctreedir, 'html')
        setup(app)

        self.assertTrue(os.path.exists(builddir))
        self.assertTrue(os.path.exists(doctreedir))

        config = app.config
        self.assertIn('sass_configs', config)
        self.assertDictEqual(config.sass_configs, {})

    def test_config(self):
        """Extension options set from config file."""
        docs = Path(os.path.join(os.path.dirname(__file__), 'docs'))
        srcdir = docs / 'source'
        builddir = docs / 'build'
        doctreedir = builddir / '.doctrees'

        with open(os.path.join(FIXTURES, 'conf.py'), 'r') as file_in:
            conf = file_in.read()
            env = {}
            exec(conf, None, env)
            expected = env['sass_configs']
        self.fs.create_dir(srcdir)
        app = Sphinx(
            srcdir, FIXTURES, builddir, doctreedir, 'html')
        config = app.config
        app.builder.cleanup()

        self.assertTrue(os.path.exists(builddir))
        self.assertTrue(os.path.exists(doctreedir))

        self.assertIn('sass_configs', config)
        self.assertDictEqual(config.sass_configs, expected)
