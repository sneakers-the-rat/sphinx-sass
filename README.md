# Sphinxcontrib-sass-compile


**Sphinxcontrib-sass-compile** is a [Sphinx](http://www.sphinx-doc.org/en/master/) extension
which enables compilation of [SASS](https://sass-lang.com/) and SCSS files to CSS
when generating Sphinx documentation.

## Usage

### Configuration in `conf.py`

To configure the extension from `conf.py`
use the `sass_compile_configs`
variable.
This is a dictionary of dictionaries,
where each subdictionary is a separate configuration.
Configuration names must be unique.


    sass_compile_configs = {
        'config_name': {
            entry='main.scss',
            output='compiled.css',
            compile_options=dict(
                ...
            ),
            variables=dict(
                'error': '#ff0000'
            ),
            add_css_file=False
        }
    )

- `entry`:
  The path to the main SASS/SCSS file.
  This may be relative to the directory
  where the document is being compile,
  or an absoulte path.
- `output`:
  The path to the resulting CSS file.
  This should be relative to the first
  entry specified in `html_static_path`
- `compile_options`:
  Options passed to the `compile`
  function from [`libsass`](https://github.com/sass/libsass-python).
  Note that all source map options are ignored.
  To generate source maps see below.
- `variables`:
  A dictionary which will be converted into SASS variables
  and inserted before the contents of the file specified
  in `entry`. The prefix `$` is not needed.
- `add_css_file`:
  By default, the extension will automatically tell Sphinx
  to add a link to the compiled CSS file.
  If this is not wanted, adding this key and setting
  it to `False` will not add the link.
- `source_maps`:
  Generate CSS source maps.
  Source maps are always embedded in the CSS output file.

### Configuration from an extension.

To use `sass_compile` in an extension,
it is necessary to connect to the `config-inited`
event (note this only available from Sphinx v1.8):

    def setup(app):
        app.setup_extension('sphinx_sass')
        app.connect('config-inited', init)

    def init(app, config):
        config.sass_compile_configs['custom-config'] = dict(
           # configuration
        )

The configuration is the same as when used
in `conf.py`, except that the
`entry` path should be an absolute path.

### Notes

- **sass_compile** uses the first
  entry in the configuration variable `html_static_path`, if it exists.
- Compiled CSS files are written directly to
  the build directory just before Sphinx
  exits (during the `build-finished`) event.
- **sass_compile** is pre-alpha. It should just work as is, but bugs are likely and anything or everything may change with absolutely no warning.

# Acknowledgements

This extension makes use of the
rather excellent [`libsass`](https://github.com/sass/libsass-python) package.
