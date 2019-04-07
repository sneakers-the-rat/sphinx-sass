.. include:: defs.rst

.. _configuration:

Configuration
=============

There are two ways that |package-name| can be configured
depending on whether the extension is being
configured from ``conf.py`` or from another
extension which utilises |package-name|.

Configure using ``conf.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To configure the extension from ``conf.py``
add ``'sphinx_sass'`` to the ``extensions`` list
and add the ``sass_configs`` variable.
This is a list of dictionaries,
where each dictionary is a separate configuration.

.. code:: python

    extensions = [
        # Other extensions...
        'sphinx_sass'
    ]

    # Other Sphinx options...

    sass_configs = [
        dict=(
           # Configuration options.
        )
    ]

For configuration options, see `Configuration options`_ below.

Configure an extension
~~~~~~~~~~~~~~~~~~~~~~

To use |package-name| in an extension,
it is necessary to connect to the ``config-inited``
event (note this only available from Sphinx v1.8):

.. code::

    def setup(app):
       app.setup_extension('sphinx-sass')
       app.connect('config-inited', init)

    def init(app, config):
       config.sass_compile_configs.insert(
           0,
           dict(
               # Configuration options.
           ))

.. note::

    While the configuration options are the same as for
    those in ``conf.py`` (see `Configuration options`_ below),
    the ``entry`` path should be an absolute path.

Configuration options
~~~~~~~~~~~~~~~~~~~~~

``entry``
   The path to the main SASS/SCSS file which whil be the
   entry point for the SASS compile.
   This may be relative to the directory
   containing the Sphinx ``conf.py`` file,
   or an absoulte path (an absolute path is required
   if |package-name| is configured from another extension).

``output``
   The path (including the filename) to the resulting CSS file.
   This should be relative to the first entry
   specified in ``html_static_path``

``compile_options``
   Options passed to the |sass.compile| function from |libsass-python|.
   The ``string``, ``filename`` and ``directory`` options
   are ignored
   (internally |package-name| uses the ``filename`` option).

   Note that correctly configuring an external source map
   can be a little unintuitive, so a convenience
   ``source_map`` option (described below)
   can be used if external source maps are required.

``add_css_file``
   By default, the extension will automatically tell Sphinx to add a
   link to the compiled CSS file. If this is not wanted
   (e.g., if the CSS file is specified in a template),
   then adding this key and setting it to ``False`` will not
   add the link.

``source_map``
   A convenience option for automatically setting the SASS ``compile_options``
   for source maps. Setting this option to the value ``embed``
   will generate embedded source maps.
   Using the value ``file`` will generate an external source map
   in the same directory as the CSS file specified with
   the ``output`` option, using the CSS filename suffixed
   with ``.map``
   (so the source map for ``main.css`` will be called ``main.css.map``).

   It is also possible to override source map settings using
   the environment variable ``SPHINX_SASS_SOURCE_MAPS``.
   This can be used, for example, in a Makefile to
   override settings in ``conf.py``:

   .. code-block:: make

      docs-dist:
	      export SPHINX_SASS_SOURCE_MAPS=FALSE; \
	      sphinx-build -b html source build

Passing variables to the SASS compiler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In rare cases, it may be desirable to pass
variables from ``conf.py`` (or an extension initialisation function)
to the SASS compiler. This can be achieved using
|importer callbacks|.

For example, given the entry point ``main.scss``:

.. code-block:: scss2

   @import "abstract";
   $headline: red !default;
   h1 {
      color: $headline;
   }


A custom importer can be defined which will be called whenever
the compiler encouters the ``@import`` statement:

.. code:: python

   def abstract_importer(path, prev):
       if path == 'abstract':
          return (path, '$headline: blue;')
       # Handled by other importers, or by default libsass behaviour
       return None

This can be added to the compile options using the
``importers`` option as a 2-tuple comprising
an integer and the importer name:

.. code:: python

   compile_options = dict(
      importers=[(0, abstract_importer)]
   )

The integer value represents the
relative priority of the custom importer
(if multiple importers are active, this is used
to determine the order in which they are applied).
When compiled, the return value of the ``abstract_importer``
will be imported.
