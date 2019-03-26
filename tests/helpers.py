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

import cssutils
from docutils.parsers.rst import directives, roles
from pyfakefs.fake_filesystem_unittest import TestCase
import sphinx.util.pycompat
import sphinx.config
from sphinx.application import Sphinx


import tests.fixtures


FIXTURES = tests.fixtures.__path__._path[0]  # pylint: disable=protected-access

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


class BaseSphinxTestCase(TestCase):
    """Base test class helper for testing with Sphinx."""

    def setUp(self):
        self.setUpPyfakefs(
            modules_to_reload=[sphinx.util.pycompat, sphinx.config])
        packages = [
            path for path in sys.path if path.endswith('site-packages')]
        for package in packages:
            self.fs.add_real_directory(package)
        self.fs.add_real_directory(FIXTURES)
        clear_docutils_cache()

        docs = Path('docs')
        self.srcdir = docs / 'source'
        self.confdir = None
        self.outdir = docs / 'build'
        self.doctreedir = self.outdir / '.doctrees'

        self.fs.create_dir(self.srcdir)

    def get_sphinx_app(self, **kwargs):
        """Helper for creating test sphinx app."""
        srcdir = kwargs.pop('srcdir', self.srcdir)
        confdir = kwargs.pop('confdir', self.confdir)
        outdir = kwargs.pop('outdir', self.outdir)
        doctreedir = kwargs.pop('doctreedir', self.doctreedir)
        status = kwargs.pop('status', None)
        warning = kwargs.pop('warning', None)
        return Sphinx(
            srcdir, confdir, outdir, doctreedir, 'html', status=status, warning=warning, **kwargs)


def parse_css(css):
    """Helper to parse a CSS file or string to a dictionary."""
    try:
        with open(css, 'r') as file_in:
            content = file_in.read()
    except FileNotFoundError:
        content = css
    sheet = cssutils.parseString(content)
    rules = {}
    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            selectors = [
                selector.selectorText for selector in rule.selectorList]
            properties = {}
            for style in rule.style:
                properties[style.name] = style.value

            for selector in rule.selectorList:
                if selector in rules:
                    rules.selector.update(**properties)
                else:
                    rules[selector.selectorText] = properties
    return rules
