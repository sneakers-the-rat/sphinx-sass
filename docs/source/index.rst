
|Package-name|
==============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

|Package-name| is a |Sphinx| extension
which enables compilation of |SASS| and SCSS files to CSS
when generating documentation.

Usage
-----

There are two ways that |package-name| can be configured:

Configuration from ``conf.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To configure the extension from ``conf.py``
use the ``sass_compile_configs`` variable.
This is a dictionary of dictionaries,
where each subdictionary is a separate configuration.

.. code:: python

    sass_compile_configs['config_name'] = dict(
       entry='main.scss',
       output='compiled.css',
       compile_options=dict(
          ...
       ),
       variables=dict(
          'error': '#ff0000'
       ),
       stylesheet=False
    )

The configuration options are as follows:

- ``entry``
   The path to the main SASS/SCSS file.
   This may be relative to the directory
   where the document is being compile,
   or an absoulte path.
- ``output``
   The path to the resulting css file.
   This should be relative to the first
   entry specified in ``html_static_path``
- ``compile_options``
   Options passed to the ``compile``
   function from |libsass|.
   Note that source map options are
   currently ignored.
- ``variables``
   A dictionary which will be converted into SASS variables
   and inserted before the contents of the file specified
   in ``entry``. The prefix ``$`` is not needed.
- ``stylesheet``
   By default, the extension will automatically tell Sphinx
   to add a link to the compiled CSS file.
   If this is not wanted, adding this key and setting
   it to ``False`` will not add the link.

Configuration from an extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use |package-name| in an extension,
it is necessary to connect to the ``config-inited``
event (note this only available from Sphinx v1.8):

.. code::

    def setup(app):
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
