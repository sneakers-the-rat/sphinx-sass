"""
    test_sphinx_sass
    ~~~~~~~~~~~~~~~~
    Tests for :mod:`sphinx_sass.__init__` module.
"""

import os
from pathlib import Path
import tempfile
import unittest

import cssutils
from docutils.parsers.rst import directives, roles
from sphinx.application import Sphinx


from .fixtures import FIXTURES

with open(os.path.join(FIXTURES, 'conf.template.py'), 'r') as _file_in:
    CONF_PY = _file_in.read()


def clear_docutils_cache():
    """Clear docutils cache for directives and roles."""
    directives._directives = {}  # pylint: disable=protected-access
    roles._roles = {}  # pylint: disable=protected-access


def make_conf_py(extensions=None, sass_configs=None):
    """Create a custom conf_py from a template."""
    conf_py = CONF_PY
    if extensions:
        conf_py = conf_py.replace('# __extensions__', repr(extensions)[1:-1])
    if sass_configs:
        conf_py = conf_py.replace(
            '# __sass_configs__', 'sass_configs = {}'.format(repr(sass_configs)))
    return conf_py


class BaseSphinxTestCase(unittest.TestCase):
    """Base test class helper for testing with Sphinx."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        tmpdir = Path(self.tmpdir.name)
        docs = tmpdir / 'docs'
        self.srcdir = docs / 'source'
        self.confdir = None
        self.outdir = docs / 'build'
        self.doctreedir = self.outdir / '.doctrees'
        os.makedirs(str(self.srcdir), exist_ok=True)

        clear_docutils_cache()

    def tearDown(self):
        self.tmpdir.cleanup()

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

    @staticmethod
    def create_file(path, mode='w', contents='', **kwargs):
        try:
            with open(path, mode, **kwargs) as file_out:
                file_out.write(contents)
        except TypeError:
            with path.open(mode, **kwargs) as file_out:
                file_out.write(contents)


def parse_css(css, raw=False):
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

            properties = {}
            for style in rule.style:
                properties[style.name] = style.value

            for selector in rule.selectorList:
                if selector in rules:
                    rules[selector].update(**properties)
                else:
                    rules[selector.selectorText] = properties

    if raw:
        return rules, content
    return rules
