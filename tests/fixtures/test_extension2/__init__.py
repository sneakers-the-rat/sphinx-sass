"""
    Extension for testing
    ~~~~~~~~~~~~~~~~~~~~~
"""
import os

WHERE_AM_I = os.path.abspath(os.path.dirname(__file__))

SASS_CONFIG = dict(
    entry=os.path.join(WHERE_AM_I, 'test_extension2.scss'),
    output='test_extension2.css')


def init(_app, config):
    config.sass_configs.append(SASS_CONFIG)


def setup(app):
    """Setup up the test extension."""
    # Also set up extension 1 as a dependency.
    app.setup_extension('sphinxcontrib.sass')
    app.setup_extension('tests.fixtures.test_extension1')
    app.connect('config-inited', init)
