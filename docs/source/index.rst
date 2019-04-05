.. include:: defs.rst

.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   configuration
   license

|package-name|
==============

Documentation for v\ |release|.

|license| |build status| |coverage|


|Package-name| is a |Sphinx| extension
which uses the Python binding of |libsass-python|
to compule |SASS| and SCSS files to CSS
when generating documentation for HTML output.

Usage
-----

After :ref:`installation <installation>`,
and assuming a basic Sphinx documentation file structure something like this:

.. code::

   docs/
   ├── _static/
   ├── source/
   │   ├── index.rst
   │   └── conf.py
   ├── styles/
   │   └── main.scss
   └── Makefile

then the simplest :ref:`configuraton <configuration>`
of the extension in ``conf.py`` could be:


.. code-block:: python

   extensions = [
       # Other Sphinx extensions...
       'sphinx_sass',
   ]

   # Other Sphinx options...
   html_static_path = ['_static']

   sass_configs = [
       dict=(
           entry='style/main.scss',
           output='sphinx_sass.css'
       )
   ]


When :program:`sphinx-build` is run with the HTML builder,
the file `main.scss` will be compiled and written to ``_static/sphinx_sass.css``
in the build directory just before Sphinx exists
(during the ``build-finished`` event).
In addition, a link to the the compiled
CSS file will be automatically added to the ``head`` tag
of each HTML page.


Acknowledgements
----------------

This extension makes use of the
rather excellent |libsass-python| package.
