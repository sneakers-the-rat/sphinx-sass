"""
    Sphinx Interface
    ~~~~~~~~~~~~~~~~

"""

import os
import tempfile

import sass


def run_sass(app, _exception):
    """Setup sass."""
    configs = app.config.sass_configs
    for config in configs.values():
        compile_sass_config(app, config)


def compile_sass_config(app, config):
    """Compile sass for a particular configuration."""
    build_dir = app.outdir
    static_dir = app.config.html_static_path[0]
    output = os.path.join(build_dir, static_dir, config['output'])

    compile_sass(
        str(config['entry']),
        str(output),
        config.get('compile_options', {}),
        sass_vars=config.get('sass_vars'))


def compile_sass(entry, output, compile_options=None, sass_vars=None):
    """Compile sass."""

    entry = str(entry)
    output = str(output)
    compile_options = compile_options or {}

    for option in ['filename', 'string', 'filename', 'source_map_filename']:
        compile_options.pop(option, None)

    include_paths = [os.path.dirname(entry)]
    include_paths.extend(compile_options.pop('include_paths', []))
    compile_options['include_paths'] = include_paths

    header = ''
    if sass_vars:
        header = '\n'.join(['${}:{};'.format(var, val)
                            for var, val in sass_vars.items()])
        header += '\n@import"{}";\n'.format(os.path.abspath(entry))

    with open(entry, 'r') as file_in:
        source = file_in.read()

    css = ''
    if source.strip():
        source = header + source
        css = sass.compile(
            string=source,
            **compile_options)

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
    app.add_config_value('sass_configs', {}, 'env')
    app.connect('build-finished', run_sass)
