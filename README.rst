|Package-name|
==============

|build status| |coverage|

|Package-name| is a |Sphinx| extension
which enables compilation of |SASS| and SCSS files to CSS
when generating documentation for HTML output.


Usage
-----

There are two ways that |package-name| can be configured:

Configuration from ``conf.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To configure the extension from ``conf.py``
use the ``sass_configs`` variable.
This is a dictionary of dictionaries,
where each subdictionary is a separate configuration.
Configuration names must be unique, an
error will be raised if a duplicate name
is encountered.

.. code:: python

    sass_configs['config_name'] = dict(
       entry='main.scss',
       output='compiled.css',
       compile_options=dict(
          ...
       ),
       add_css_file=False,
       source_map='embed'
    )

The configuration options are as follows:

- ``entry``
   The path to the main SASS/SCSS file.
   This may be relative to the directory
   containing the Sphinx ``conf.py`` file,
   or an absoulte path.
- ``output``
   The path to the resulting css file.
   This should be relative to the first
   entry specified in ``html_static_path``
- ``compile_options``
   Options passed to the ``compile``
   function from |libsass|.
   Note that correctly configuration an external source map
   can be a little unintuitive, so it is
   recommended that ``source_map`` option
   described below be used if external source maps
   are required.
- ``add_css_file``
   By default, the extension will automatically tell Sphinx
   to add a link to the compiled CSS file.
   If this is not wanted, adding this key and setting
   it to ``False`` will not add the link.
- ``source_map``
   A convenience option for automatticaly setting
   the ``compile_options`` for source maps.
   Setting this option to the value ``embed`` will generate
   embedded source maps. Using the value ``file``
   will generate an external source map.


Configuration from an extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use |package-name| in an extension,
it is necessary to connect to the ``config-inited``
event (note this only available from Sphinx v1.8):

.. code::

    def setup(app):
       app.setup_extension('sphinx-sass')
       app.connect('config-inited', init)

    def init(app, config):
       config.sass_compile_configs['custom-config'] = dict(
          # configuration
       )

The configuration is the same as when used
in ``conf.py``, except that the
``entry`` path should be an absolute path.

Notes
~~~~~

- |Package-name| uses the first entry in the configuration variable ``html_static_path``, if it exists.
- Compiled CSS files are written directly to the build directory just before Sphinx exits (during the ``build-finished``) event.
- |Package-name| is pre-alpha. It should just work as is, but bugs are likely and anything or everything may change with absolutely no warning.

Acknowledgements
----------------

This extension makes use of the
rather excellent |libsass| package.


.. |Package-name| replace:: **Sphinx-sass**

.. |package-name| replace:: **sphinx-sass**

.. |sphinx| replace:: Sphinx_
.. _Sphinx: https://www.sphinx-doc.org/en/master/

.. |sass| replace:: SASS_
.. _SASS: https://sass-lang.com/

.. |libsass| replace:: libsass_
.. _libsass: https://github.com/sass/libsass-python

.. |build status| image:: https://travis-ci.org/mwibrow/sphinx-sass.svg?branch=master
    :target: https://travis-ci.org/mwibrow/sphinx-sass

.. |coverage| image:: https://coveralls.io/repos/github/mwibrow/sphinx-sass/badge.svg
    :target: https://coveralls.io/github/mwibrow/sphinx-sass