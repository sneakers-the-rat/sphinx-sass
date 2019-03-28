"""
    test_sphinx_sass
    ~~~~~~~~~~~~~~~~
    Tests for :mod:`sphinx_sass.__init__` module.
"""

import os
import unittest

from sphinx_sass import (
    compile_sass,
    compile_sass_config,
    run_sass,
    setup,
    SassConfigs)

from tests.fixtures import test_extension1, test_extension2

from tests.helpers import (
    BaseSphinxTestCase,
    make_conf_py,
    parse_css)


class TestSassConfigs(unittest.TestCase):
    """Tests for the SassConfigs class."""

    def test_add(self):
        """Add configurations."""
        configs = SassConfigs()
        configs['key'] = {}
        self.assertIn('key', configs)

    def test_reject(self):
        """Duplicate key raises KeyError."""
        configs = SassConfigs()
        configs['key'] = {}
        with self.assertRaises(KeyError):
            configs['key'] = {}


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
        self.create_file(
            os.path.join(self.srcdir, 'conf.py'), contents=conf_py)

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
        self.create_file(
            os.path.join(self.srcdir, 'conf.py'), contents=conf_py)

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
        self.create_file(
            os.path.join(self.srcdir, 'conf.py'), contents=conf_py)

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

    def setUp(self):
        super().setUp()

        self.entry = os.path.join(self.srcdir, 'main.scss')
        self.output = os.path.join(self.outdir, 'main.css')
        self.create_file(
            self.entry,
            contents='$color: red !default; .document { h1, h2 { color: $color; } }')
        self.selectors = ['.document h1', '.document h2']

    def test_empty_entry(self):
        """No CSS written if SCSS file empty."""
        entry = os.path.join(self.srcdir, 'main.scss')
        output = os.path.join(self.outdir, 'main.css')
        self.create_file(entry, contents='')
        compile_sass(entry, output, {})
        self.assertFalse(os.path.exists(self.output))

    def test_css_created(self):
        """CSS file created for valid SCSS."""
        compile_sass(self.entry, self.output, {})
        self.assertTrue(os.path.exists(self.output))

        rules = parse_css(self.output)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})

    def test_sass_variables(self):
        """Custom SASS vars take precedence over in-file variables."""
        compile_sass(self.entry, self.output, sass_vars=dict(color='blue'))
        self.assertTrue(os.path.exists(self.output))

        rules = parse_css(self.output)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'blue'})

    def test_output_style(self):
        """Compile options output_style works"""
        compile_sass(
            self.entry,
            self.output,
            compile_options=dict(output_style='compressed'))
        self.assertTrue(os.path.exists(self.output))

        rules, css = parse_css(self.output, raw=True)
        self.assertEqual(css.strip(), '.document h1,.document h2{color:red}')
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})

    def test_source_map(self):
        """Compile options output_style works"""
        compile_sass(
            self.entry,
            self.output,
            compile_options=dict(source_map_embed=True))
        self.assertTrue(os.path.exists(self.output))

        rules, css = parse_css(self.output, raw=True)
        self.assertIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})


class TestCompileSassConfig(BaseSphinxTestCase):
    """Tests for the compile_sass_config function."""

    def setUp(self):
        super().setUp()

        self.entry = os.path.join(self.srcdir, 'main.scss')
        self.output = os.path.join(self.outdir, 'main.css')
        self.create_file(
            self.entry,
            contents='$color: red !default; .document { h1, h2 { color: $color; } }')
        self.selectors = ['.document h1', '.document h2']

    def test_no_source_map(self):
        """Check source_maps=False does not produce source map."""
        config = dict(
            entry=self.entry,
            output=self.output)

        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        rules, css = parse_css(self.output, raw=True)
        self.assertNotIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})

    def test_sourcemap(self):
        """Check source_maps=True does produces source map."""
        config = dict(
            entry=self.entry,
            output=self.output,
            source_maps=True)

        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        rules, css = parse_css(self.output, raw=True)
        self.assertIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})

    def test_no_source_maps_override(self):
        """Source maps not produced when environment variable overides sources_maps key."""
        config = dict(
            entry=self.entry,
            output=self.output,
            source_maps=True)
        os.environ['SPHINX_SASS_SOURCE_MAPS'] = '0'
        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        _, css = parse_css(self.output, raw=True)
        self.assertNotIn('sourceMappingURL', css)
        del os.environ['SPHINX_SASS_SOURCE_MAPS']

    def test_source_maps_override(self):
        """Source maps produced when environment variable overides sources_maps key."""
        config = dict(
            entry=self.entry,
            output=self.output,
            source_maps=False)
        os.environ['SPHINX_SASS_SOURCE_MAPS'] = '1'
        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        _, css = parse_css(self.output, raw=True)
        self.assertIn('sourceMappingURL', css)
        del os.environ['SPHINX_SASS_SOURCE_MAPS']


class TestRunSass(BaseSphinxTestCase):
    """Tests for the run_sass function."""

    def test_multiple_configs(self):
        """Multiple configs creates multiple outputs."""
        entry1 = os.path.join(self.srcdir, 'main1.scss')
        output1 = 'main1.css'
        entry2 = os.path.join(self.srcdir, 'main2.scss')
        output2 = 'main2.css'

        configs = dict(
            main1=dict(
                entry=entry1,
                output=output1),
            main2=dict(
                entry=entry2,
                output=output2,
                source_maps=True))

        self.create_file(
            entry1,
            contents='.document { h1, h2 { color: red; } }')
        self.create_file(
            entry2,
            contents='.document { h1, h2 { color: green; } }')

        conf_py = make_conf_py(
            extensions=['sphinx_sass'], sass_configs=configs)
        self.create_file(
            os.path.join(self.srcdir, 'conf.py'), contents=conf_py)
        app = self.get_sphinx_app(confdir=self.srcdir)

        run_sass(app, None)

        selectors = ['.document h1', '.document h2']

        rules, css = parse_css(
            os.path.join(self.outdir, '_static', output1), raw=True)
        self.assertNotIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})

        rules, css = parse_css(
            os.path.join(self.outdir, '_static', output2), raw=True)
        self.assertIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'green'})
