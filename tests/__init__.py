project = 'sphinx-sass-tests'
copyright = '2019, Mark Wibrow'
author = 'Mark Wibrow'
version = ''
release = ''
extensions = [
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = []
pygments_style = None
html_theme = 'alabaster'
html_theme_options = {
    'nosidebar': True,
}
html_static_path = ['_static']
htmlhelp_basename = 'sphinx-sass-doc'
latex_elements = {}
latex_documents = [
    (master_doc, 'sphinx-sass-tests.tex', 'sphinx-sass-tests Documentation',
     'Mark Wibrow', 'manual'),
]
man_pages = [
    (master_doc, 'sphinx-sass-tests', 'sphinx-sass-tests Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'sphinx-sass-tests', 'sphinx-sass-tests Documentation',
     author, 'sphinx-sass-tests', 'One line description of project.',
     'Miscellaneous'),
]
epub_title = project
epub_exclude_files = ['search.html']
