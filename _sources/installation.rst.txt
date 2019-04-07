.. include:: defs.rst

.. _installation:

Installation
============

|Package-name| is compatible with |Python| versions >=3.6 and |Sphinx| >=1.8,
and should work anywhere that Python and |libsass-python| can be installed.

.. note::

    |Package-name| depends on |libsass-python|, which in turn depends on
    |libsass|.
    This latter dependency requires a recent C++ compiler
    (see the |libsass-readme| for the libsass project for details).


Install from GitHub
-------------------------

To install |package-name| directly from the GitHub |repository| using :program:`pip`:

.. code-block:: console

   $ pip install git+https://github.com/mwibrow/sphinx-sass.git

Alternatively, clone the repository and run the set-up script manually:

.. code-block:: console

    $ git clone https://github.com/mwibrow/sphinx-sass.git
    $ cd sphinx-sass
    $ python setup.py install
