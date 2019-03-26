"""
    Extension for testing
    ~~~~~~~~~~~~~~~~~~~~~
"""
import os

WHERE_AM_I = os.path.abspath(os.path.dirname(__file__))


def init(app, config):
    config.sass_configs['test_ext1'] = dict(
        entry=os.path.join(WHERE_AM_I, 'test_ext1.scss'),
        output='test_ext1.css'
    )


def setup(app):
    """Setup up the test extension."""
    app.connect('config-inited', init)
