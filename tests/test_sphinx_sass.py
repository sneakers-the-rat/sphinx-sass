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

from sphinx_sass import compile_sass, setup

import tests.fixtures
from tests.fixtures import test_extension1, test_extension2

from tests.helpers import (
    BaseSphinxTestCase,
    clear_docutils_cache,
    make_conf_py,
    parse_css)


class TestSetup(BaseSphinxTestCase):
    """Test the setup function."""

    def test_setup(self):
        """Extension setup adds extension options."""

        app = self.get_sphinx_app(confdir=None)
        setup(app)

        self.assertTrue(os.path.exists(self.outdir))
        self.assertTrue(os.path.exists(self.doctreedir))

        config = app.config
        self.assertIn('sass_configs', config)
        self.assertDictEqual(config.sass_configs, {})


class TestConfig(BaseSphinxTestCase):
    """Test the various configurations."""

    def test_config(self):
        """Extension options set from config file."""

        expected = dict(
            test=dict(
                entry='test.scss',
                output='test.css'
            ))

        conf_py = make_conf_py(
            extensions=['sphinx_sass'], sass_configs=expected)
        self.fs.create_file(self.srcdir / 'conf.py', contents=conf_py)

        app = self.get_sphinx_app(confdir=self.srcdir)

        self.assertTrue(os.path.exists(self.outdir))
        self.assertTrue(os.path.exists(self.doctreedir))

        config = app.config
        self.assertIn('sass_configs', config)
        self.assertDictEqual(config.sass_configs, expected)

        css_file = app.registry.css_files[0][0]
        self.assertEqual(css_file, expected['test']['output'])

    def test_extension_config(self):
        """Extension options set from another extension."""

        conf_py = make_conf_py(
            extensions=['tests.fixtures.test_extension1'])
        self.fs.create_file(self.srcdir / 'conf.py', contents=conf_py)

        app = self.get_sphinx_app(confdir=self.srcdir)

        self.assertTrue(os.path.exists(self.outdir))
        self.assertTrue(os.path.exists(self.doctreedir))

        config = app.config
        ext = test_extension1
        self.assertIn('sass_configs', config)
        self.assertIn(ext.CONFIG_NAME, config.sass_configs)
        self.assertDictEqual(
            ext.SASS_CONFIG, config.sass_configs[ext.CONFIG_NAME])

        css_file = app.registry.css_files[0][0]
        self.assertEqual(css_file, ext.SASS_CONFIG['output'])

    def test_extensions_config(self):
        """Extension options set from multiple extensions."""

        conf_py = make_conf_py(
            extensions=[
                'tests.fixtures.test_extension1',
                'tests.fixtures.test_extension2',
            ])
        self.fs.create_file(self.srcdir / 'conf.py', contents=conf_py)

        app = self.get_sphinx_app(confdir=self.srcdir)

        self.assertTrue(os.path.exists(self.outdir))
        self.assertTrue(os.path.exists(self.doctreedir))

        config = app.config
        self.assertIn('sass_configs', config)

        ext = test_extension1
        self.assertIn(ext.CONFIG_NAME, config.sass_configs)
        self.assertDictEqual(
            ext.SASS_CONFIG, config.sass_configs[ext.CONFIG_NAME])
        css_file = app.registry.css_files[0][0]
        self.assertEqual(css_file, ext.SASS_CONFIG['output'])

        ext = test_extension2
        self.assertIn(ext.CONFIG_NAME, config.sass_configs)
        self.assertDictEqual(
            ext.SASS_CONFIG, config.sass_configs[ext.CONFIG_NAME])
        css_file = app.registry.css_files[1][0]
        self.assertEqual(css_file, ext.SASS_CONFIG['output'])


class TestCompileSass(BaseSphinxTestCase):
    """Tests for the :func:`compile_sass` function."""

    def test_empty_entry(self):
        """No CSS written if SCSS file empty."""
        entry = self.srcdir / 'main.scss'
        output = self.outdir / 'main.css'
        self.fs.create_file(entry, contents='')
        compile_sass(entry, output, {}, {})
        self.assertFalse(os.path.exists(output))

    def test_css_created(self):
        """CSS file created for valid SCSS."""
        entry = self.srcdir / 'main.scss'
        output = self.outdir / 'main.css'
        self.fs.create_file(
            entry,
            contents='$color: red !default; body { h1, h2 { color: $color; } }')
        compile_sass(entry, output, {}, {})
        self.assertTrue(os.path.exists(output))

        rules = parse_css(output)
        self.assertIn('body h1', rules)
        self.assertDictEqual(rules['body h1'], {'color': 'red'})
