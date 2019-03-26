"""
    Extension for testing
    ~~~~~~~~~~~~~~~~~~~~~
"""
import os

WHERE_AM_I = os.path.abspath(os.path.dirname(__file__))

CONFIG_NAME = 'test_ext1'
SASS_CONFIG = dict(
    entry=os.path.join(WHERE_AM_I, 'test_ext1.scss'),
    output='test_ext1.css')


def init(app, config):
    config.sass_configs[CONFIG_NAME] = SASS_CONFIG


def setup(app):
    """Setup up the test extension."""
    app.setup_extension('sphinx_sass')
    app.connect('config-inited', init)
