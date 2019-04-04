"""
Nox config file.
"""

import nox


@nox.session
def lint(session):
    """
    Lint
    """
    session.install('-r', 'requirements.txt')
    session.install('-r', 'requirements-dev.txt')
    session.env['PYTHONPATH'] = '.'
    session.run('pylint', 'sphinxcontrib', 'tests')


@nox.session(python=['3.6'])
def test(session):
    """
    Test
    """
    session.install('-r', 'requirements.txt')
    session.install('-r', 'requirements-dev.txt')
    session.env['PYTHONPATH'] = '.'
    session.run(
        'py.test',
        '--cov=sphinxcontrib.sass',
        '--cov-report=term-missing',
        'tests')
