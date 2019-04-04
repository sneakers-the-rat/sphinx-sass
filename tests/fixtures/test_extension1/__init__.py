"""
    Extension for testing
    ~~~~~~~~~~~~~~~~~~~~~
"""
import os

WHERE_AM_I = os.path.abspath(os.path.dirname(__file__))

SASS_CONFIG = dict(
    entry=os.path.join(WHERE_AM_I, 'test_extension1.scss'),
    output='test_extension1.css')


def init(_app, config):
    config.sass_configs.append(SASS_CONFIG)


def setup(app):
    """Setup up the test extension."""
    app.setup_extension('sphinx_sass')
    app.connect('config-inited', init)
