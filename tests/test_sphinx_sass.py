"""
    test_sphinx_sass
    ~~~~~~~~~~~~~~~~
    Tests for :mod:`sphinx_sass.__init__` module.
"""

import os

from sphinxcontrib.sass import (
    chdir,
    compile_sass,
    compile_sass_config,
    run_sass,
    setup)

from tests.fixtures import test_extension1, test_extension2

from tests.helpers import (
    BaseSphinxTestCase,
    get_source_mapping_url,
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
        self.assertCountEqual(config.sass_configs, [])


class TestConfig(BaseSphinxTestCase):
    """Test the various configurations."""

    def test_config(self):
        """Extension options set from config file."""

        expected = dict(entry='test.scss', output='test.css')

        conf_py = make_conf_py(
            extensions=['sphinxcontrib.sass'], sass_configs=[expected])
        self.create_file(
            os.path.join(self.srcdir, 'conf.py'), contents=conf_py)

        app = self.get_sphinx_app(confdir=self.srcdir)

        self.assertTrue(os.path.exists(self.outdir))
        self.assertTrue(os.path.exists(self.doctreedir))

        config = app.config
        self.assertIn('sass_configs', config)
        self.assertIn(expected, config.sass_configs)

        css_file = app.registry.css_files[0][0]
        self.assertEqual(css_file, expected['output'])

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
        self.assertIn(ext.SASS_CONFIG, config.sass_configs)

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
        self.assertIn(ext.SASS_CONFIG, config.sass_configs)
        css_file = app.registry.css_files[0][0]
        self.assertEqual(css_file, ext.SASS_CONFIG['output'])

        ext = test_extension2
        self.assertIn(ext.SASS_CONFIG, config.sass_configs)
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
        self.create_file(entry, contents='')
        css, srcmap = compile_sass(entry)

        self.assertFalse(css)
        self.assertFalse(srcmap)

    def test_css_emited(self):
        """CSS created for valid SCSS."""
        css, srcmap = compile_sass(self.entry)

        rules = parse_css(css)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})
        self.assertFalse(srcmap)

    def test_output_style(self):
        """Compile options output_style works"""
        css, srcmap = compile_sass(
            self.entry,
            compile_options=dict(output_style='compressed'))

        rules = parse_css(css)
        self.assertEqual(css.strip(), '.document h1,.document h2{color:red}')
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})
        self.assertFalse(srcmap)

    def test_interal_source_map(self):
        """Compile embedded source map"""
        css, srcmap = compile_sass(
            self.entry,
            compile_options=dict(source_map_embed=True))

        rules = parse_css(css)
        self.assertIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})
        self.assertFalse(srcmap)

    def test_external_source_map(self):
        """Compile external source map"""
        css, srcmap = compile_sass(
            self.entry,
            compile_options=dict(source_map_filename='main.css.map'))

        rules = parse_css(css)
        self.assertIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})
        self.assertGreater(len(srcmap), 0)


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

    def test_relative_entry_path(self):
        """Test relative entry path."""

        entry = os.path.basename(self.entry)
        with chdir(os.path.dirname(self.entry)):
            self.create_file(
                entry,
                contents='$color: red !default; .document { h1, h2 { color: $color; } }')

        config = dict(
            entry=entry,
            output=self.output)

        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        self.assertTrue(os.path.exists(self.output))
        rules, css = parse_css(self.output, raw=True)
        self.assertNotIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})

    def test_no_source_map(self):
        """Check defaults do not produce source map."""
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

    def test_embedded_source_map(self):
        """Check embeded source map produced."""
        config = dict(
            entry=self.entry,
            output=self.output,
            compile_options=dict(source_map_embed=True))

        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        rules, css = parse_css(self.output, raw=True)
        self.assertIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})

    def test_external_source_maps(self):
        """Check external source maps produced"""
        config = dict(
            entry=self.entry,
            output=self.output,
            compile_options=dict(
                source_map_filename='main.css.map'
            ))
        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        _, css = parse_css(self.output, raw=True)
        self.assertIn('sourceMappingURL', css)
        self.assertTrue(os.path.exists(
            os.path.join(os.path.dirname(self.output), 'main.css.map')))

    def test_external_source_maps_different_path(self):
        """Check external source maps produced with different path"""

        source_map_filename = os.path.join('maps', 'main.css.map')
        config = dict(
            entry=self.entry,
            output=self.output,
            compile_options=dict(
                source_map_filename=source_map_filename
            ))
        app = self.get_sphinx_app()
        compile_sass_config(app, config)

        _, css = parse_css(self.output, raw=True)
        self.assertIn('sourceMappingURL', css)

        srcmap_url = get_source_mapping_url(css)
        self.assertEqual(srcmap_url, source_map_filename)

        self.assertTrue(os.path.exists(
            os.path.join(
                os.path.dirname(self.output), source_map_filename)))

    def test_embedded_source_map_config(self):
        """Check embeded source map produced using config option"""
        config = dict(
            entry=self.entry,
            output=self.output,
            source_map='embed')

        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        rules, css = parse_css(self.output, raw=True)
        self.assertIn('sourceMappingURL', css)
        self.assertEqual(len(rules), 2)
        for selector in self.selectors:
            self.assertIn(selector, rules)
            self.assertDictEqual(rules[selector], {'color': 'red'})

    def test_external_source_maps_config(self):
        """Check external source maps produced using config option"""
        config = dict(
            entry=self.entry,
            output=self.output,
            source_map='file')
        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        _, css = parse_css(self.output, raw=True)
        self.assertIn('sourceMappingURL', css)
        self.assertTrue(os.path.exists(
            os.path.join(os.path.dirname(self.output), 'main.css.map')))

    def test_no_source_maps_override(self):
        """Source maps not produced when environment variable overides compile options"""
        config = dict(
            entry=self.entry,
            output=self.output)
        os.environ['SPHINX_SASS_SOURCE_MAPS'] = '0'
        app = self.get_sphinx_app()
        compile_sass_config(app, config)
        _, css = parse_css(self.output, raw=True)
        self.assertNotIn('sourceMappingURL', css)
        del os.environ['SPHINX_SASS_SOURCE_MAPS']

    def test_source_maps_override(self):
        """Source maps produced when environment variable overides compile options"""
        config = dict(
            entry=self.entry,
            output=self.output,
            compile_options=dict(
                source_map_embed=True
            ))
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

        configs = [
            dict(
                entry=entry1,
                output=output1),
            dict(
                entry=entry2,
                output=output2,
                compile_options=dict(
                    source_map_embed=True))]

        self.create_file(
            entry1,
            contents='.document { h1, h2 { color: red; } }')
        self.create_file(
            entry2,
            contents='.document { h1, h2 { color: green; } }')

        conf_py = make_conf_py(
            extensions=['sphinxcontrib.sass'], sass_configs=configs)
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
