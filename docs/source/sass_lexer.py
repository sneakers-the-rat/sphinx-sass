"""
    Custom SCSS lexer
    ~~~~~~~~~~~~~~~~~

    This is an alternative to the Pygments SCSS lexer
    which is broken.

    Note, this SCSS lexer is also broken, but just a bit less
    broken.
"""
import re
from pygments.lexer import ExtendedRegexLexer
from pygments.lexers.css import (
    bygroups, copy, Comment, default, include, iteritems, Keyword,
    Name, Operator, Punctuation, String, Text)
from pygments.lexers.css import ScssLexer as DefaultScssLexer


class ScssLexer(ExtendedRegexLexer):
    """
    For SCSS stylesheets.
    """

    name = 'SCSS2'
    aliases = ['scss2']
    filenames = ['*.scss']
    mimetypes = ['text/x-scss']

    flags = re.IGNORECASE | re.DOTALL

    def selector_callback(self, match, ctx):
        ctx.pos = match.start()

        stack = ctx.stack
        ctx.stack = ['selector']
        analyses = []
        try:
            for pos, token, text in self.get_tokens_unprocessed(context=ctx):
                analyses.append((pos, token, text))
        except IndexError:
            pass
        text = ''.join(analysis[-1] for analysis in analyses).strip()
        if text and text[-1] in ';}':
            analyses = []
            ctx.pos = match.start()
            ctx.stack = ['attribute']
            try:
                for pos, token, text in self.get_tokens_unprocessed(context=ctx):
                    analyses.append((pos, token, text))
            except IndexError:
                pass
        for pos, token, text in analyses:
            yield pos, token, text
        ctx.stack = stack
        ctx.pos = pos + len(text)

    tokens = {}

    for group, common in iteritems(DefaultScssLexer.tokens):
        tokens[group] = copy.copy(common)

    tokens['root'] = [
        (r'\s+', Text),
        (r'//.*?\n', Comment.Single),
        (r'/\*.*?\*/', Comment.Multiline),
        (r'@import', Keyword, 'value'),
        (r'@for', Keyword, 'for'),
        (r'@if', Keyword, 'condition'),
        (r'@while', Keyword, 'condition'),
        (r'@else', Keyword),
        (r'@(debug|warn|if|while)', Keyword, 'value'),
        (r'(@mixin)( [\w-]+)', bygroups(Keyword, Name.Function), 'value'),
        (r'(@include)( [\w-]+)', bygroups(Keyword, Name.Decorator), 'value'),
        (r'@extend', Keyword, 'selector'),
        (r'(@media)(\s+)', bygroups(Keyword, Text), 'value'),
        (r'@[\w-]+', Keyword, 'selector'),
        (r'(\$[\w-]*\w)([ \t]*:)', bygroups(Name.Variable, Operator), 'value'),
        (r'[{}]', Punctuation),
        (r'[\w\.#]', selector_callback),
    ]
    tokens['selector'] = [
        (r'[ \t]+', Text),
        (r'\:', Name.Decorator, 'pseudo-class'),
        (r'\.', Name.Class, 'class'),
        (r'#\{', String.Interpol, 'interpolation'),
        (r'\#', Name.Namespace, 'id'),
        (r'[\w-]+', Name.Tag),
        (r'[~^*!&\[\]()<>|+=@:./?-]', Operator),
        (r'"', String.Double, 'string-double'),
        (r"'", String.Single, 'string-single'),
        (r'[,{;]', Punctuation, '#pop')
    ]
    tokens['attribute'] = [
        (r'\s+', Text),
        (r'[\w-]+', Name.Attribute),
        (r'#\{', String.Interpol, 'interpolation'),
        (r'[:]', Operator, 'value'),
        (r'\}', Punctuation, '#pop')
    ]
    tokens['condition'] = [
        (r'[!%()<>+=-]', Operator),
        include('value'),
        default('#pop')]
    tokens['else'] = [('if', Keyword, 'condition'), default('#pop')]
    tokens['value'].append((r'\$[\w-]', Name.Variable))
    tokens['value'].append((r'}', Punctuation, '#pop'))
    tokens['pseudo-class'] = [
        (r'[\w-]+', Name.Decorator),
        (r'#\{', String.Interpol, 'interpolation'),
        include('value'),
        default('#pop'),
    ]
