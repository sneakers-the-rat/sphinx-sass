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
        config.get('compile_options', {}))


def compile_sass(entry, output, compile_options=None, sass_vars=None):
    """Compile sass."""

    entry = str(entry)
    output = str(output)

    sass_vars = sass_vars or {}

    if sass_vars:
        _sass = '\n'.join(['${}:{};'.format(var, val)
                           for var, val in sass_vars.items()])
        _sass += '\n@import"{}";'.format(os.path.abspath(entry))
        with tempfile.TemporaryDirectory() as tmpdir:
            _entry = os.path.join(tmpdir, '_entry.scss')
            with open(_entry) as file_out:
                file_out.write(_sass)
            _compile_sass(_entry, output, compile_options)

    else:
        _compile_sass(entry, output, compile_options)


def _compile_sass(entry, output, compile_options):

    compile_options = compile_options or {}
    compile_options.pop('filename', None)
    compile_options.pop('dirname', None)
    compile_options.pop('string', None)

    # Not needed.
    include_paths = [os.path.dirname(entry)]
    include_paths.extend(compile_options.pop('include_paths', []))

    source_map_filename = compile_options.get('source_maps_filename', None)
    source_maps = compile_options.pop(
        'source_maps', None) or source_map_filename
    source_map_output = None
    if source_maps:
        if not source_map_filename:
            components = output.split(os.path.extsep)
            components.insert(-1, 'map')
            source_map_output = os.path.extsep.join(components)
            source_map_filename = os.path.basename()
            compile_options['source_map_filename'] = source_map_output

    os.makedirs(os.path.dirname(output), exist_ok=True)

    if source_maps:
        css, source_map = sass.compile(
            filename=entry,
            include_paths=include_paths,
            **compile_options)
    else:
        css = sass.compile(
            filename=entry,
            include_paths=include_paths,
            **compile_options)
        source_map = ''

    if css.strip():
        with open(output, 'w') as file_out:
            file_out.write(css)
    if source_map.strip() and source_map_output:
        with open(source_map_output, 'w') as file_out:
            file_out.write(source_map)


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
