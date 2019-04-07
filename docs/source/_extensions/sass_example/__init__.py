"""
    Extensions for demonstrating SASS pre-processing
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


import docutils.nodes
from docutils.parsers.rst import directives, Directive
import sass


class SassExampleDirective(Directive):
    """Class for processing the :rst:dir:`sass-example` directive.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    option_spec = {
        'syntax': directives.unchanged,
        'intertext': directives.unchanged,
        'sass-only': directives.flag,
        'scss-only': directives.flag,
        'css-only': directives.flag,
        'output-style': directives.unchanged,
    }

    def run(self):
        """Compile sass.
        """

        sass_only = 'sass-only' in self.options or 'scss-only' in self.options
        css_only = 'css-only' in self.options
        is_sass = self.options.get('syntax', 'scss').lower() == 'sass'
        intertext = self.options.get('intertext')
        output_style = self.options.get('output-style', 'nested')
        scss = '\n'.join(line for line in self.content)

        css = sass.compile(string=scss, indented=is_sass, output_style=output_style)

        parent = docutils.nodes.line_block()
        if not css_only:
            node = docutils.nodes.literal_block(scss, scss)
            node['language'] = 'sass' if is_sass else 'scss2'
            parent += node
        if intertext:
            node = docutils.nodes.paragraph(intertext, intertext)
            parent += node
        if not sass_only:
            node = docutils.nodes.literal_block(css, css)
            node['language'] = 'scss2'
            parent += node

        return [parent]


def setup(app):
    app.add_directive('sass-example', SassExampleDirective)
