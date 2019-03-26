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

from docutils.parsers.rst import directives, roles

from pyfakefs.fake_filesystem_unittest import TestCase

import sphinx.util.pycompat
import sphinx.config
from sphinx.application import Sphinx

from sphinx_sass import setup

FIXTURES = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))

with open(os.path.join(FIXTURES, 'conf.template.py'), 'r') as file_in:
    CONF_PY = file_in.read()


def clear_docutils_cache():
    """Clear docutils cache for directives and roles."""
    directives._directives = {}
    roles._roles = {}


def make_conf_py(extensions=None, sass_configs=None):
    """Create a custom conf_py from a template."""
    conf_py = CONF_PY
    if extensions:
        conf_py = conf_py.replace('# __extensions__', repr(extensions)[1:-1])
    if sass_configs:
        conf_py = conf_py.replace(
            '# __sass_configs__', 'sass_configs = {}'.format(repr(sass_configs)))
    return conf_py


class TestSetup(TestCase):

    def setUp(self):
        self.setUpPyfakefs(
            modules_to_reload=[sphinx.util.pycompat, sphinx.config])
        packages = [
            path for path in sys.path if path.endswith('site-packages')]
        for package in packages:
            self.fs.add_real_directory(package)
        self.fs.add_real_directory(FIXTURES)
        clear_docutils_cache()

    def test_setup(self):
        """Extension setup adds extension options."""
        docs = Path(os.path.join(os.path.dirname(__file__), 'docs'))

        srcdir = docs / 'source'
        builddir = docs / 'build'
        doctreedir = builddir / '.doctrees'
        self.fs.create_dir(srcdir)

        app = Sphinx(
            srcdir, None, builddir, doctreedir, 'html', status=None, warning=None)
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

        expected = dict(
            test=dict(
                entry='test.scss',
                output='test.css'
            ))

        conf_py = make_conf_py(
            extensions=['sphinx_sass'], sass_configs=expected)
        self.fs.create_file(srcdir / 'conf.py', contents=conf_py)

        app = Sphinx(
            srcdir, srcdir, builddir, doctreedir, 'html', status=None, warning=None)

        config = app.config
        self.assertTrue(os.path.exists(builddir))
        self.assertTrue(os.path.exists(doctreedir))

        self.assertIn('sass_configs', config)
        self.assertDictEqual(config.sass_configs, expected)

        css_file = app.registry.css_files[0][0]
        self.assertEqual(css_file, expected['test']['output'])
