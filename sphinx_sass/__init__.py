"""
    Sphinx Interface
    ~~~~~~~~~~~~~~~~

"""

import os
import tempfile

import sass


LIBSASS_SUPPORTED_COMPILE_OPTIONS = [
    'output_style',
    'include_paths',
    'precision',
    'custom_functions',
    'indented',
    'importers'
]


class SassConfigs(dict):
    """Subclass of dict for holding SASS configs."""

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(
                'Config "{}" already in SASS configurations.'.format(key))
        super().__setitem__(key, value)


def run_sass(app, _exception):
    """Setup sass."""
    configs = app.config.sass_configs
    for config in configs.values():
        compile_sass_config(app, config)


def compile_sass_config(app, config):
    """Compile sass for a particular configuration."""
    build_dir = app.outdir
    try:
        static_dir = app.config.html_static_path[0]
    except (AttributeError, IndexError):
        static_dir = ''
    output = os.path.join(build_dir, static_dir, config['output'])

    compile_options = config.get('compile_options', {})
    compile_options = {
        key: compile_options[key] for key in LIBSASS_SUPPORTED_COMPILE_OPTIONS
        if key in compile_options}

    try:
        source_maps_env = int(os.getenv('SPHINX_SASS_SOURCE_MAPS', None))
        if source_maps_env:
            compile_options['source_map_embed'] = True
    except (TypeError, ValueError):
        if config.get('source_maps'):
            compile_options['source_map_embed'] = True

    compile_sass(
        str(config['entry']),
        str(output),
        compile_options,
        variables=config.get('variables'))


def compile_sass(entry, output, compile_options=None, variables=None):
    """Compile sass."""

    entry = str(entry)
    output = str(output)
    compile_options = compile_options or {}

    for option in ['filename', 'string', 'filename', 'source_map_filename']:
        compile_options.pop(option, None)

    include_paths = [os.path.dirname(entry)]
    include_paths.extend(compile_options.pop('include_paths', []))
    compile_options['include_paths'] = include_paths

    css, header = '', ''
    if variables:
        header = '\n'.join(['${}:{};'.format(var, val)
                            for var, val in variables.items()])
        header += '\n@import"{}";\n'.format(os.path.abspath(entry))

        with open(entry, 'r') as file_in:
            source = file_in.read()

        css = ''
        if source.strip():
            source = header + source
            css = sass.compile(string=source, **compile_options)
    else:
        css = sass.compile(filename=entry, **compile_options)

    if css.strip():
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, 'w') as file_out:
            file_out.write(css)


def init(app):
    """Set up the style sheets."""
    configs = app.config.sass_configs
    for config in configs.values():
        if config.get('add_css_file', True):
            app.add_css_file(config['output'])


def setup(app):
    """Setup the app."""
    app.connect('builder-inited', init)
    app.add_config_value('sass_configs', SassConfigs(), 'env')
    app.connect('build-finished', run_sass)
