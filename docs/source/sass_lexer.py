"""
    Custom SCSS lexer
    ~~~~~~~~~~~~~~~~~

    This is an alternative to the Pygments SCSS lexer
    which is broken.

    Note, this SCSS lexer is also broken, but just a bit less
    broken.
"""

from pygments.lexers.css import (
    bygroups, copy, default, include, iteritems, Keyword,
    Name, Operator, Punctuation, String, Text, words)
from pygments.lexers.css import ScssLexer as DefaultScssLexer

PSEUDO_CLASSES = [
    'active',
    'checked',
    'disabled',
    'empty',
    'enabled',
    'first-child',
    'first-of-type',
    'focus',
    'hover',
    'in-range',
    'invalid',
    'last-child',
    'last-of-type',
    'link',
    'only-of-type',
    'only-child',
    'optional',
    'out-of-range',
    'read-only',
    'read-write',
    'required',
    'root',
    'target',
    'valid',
    'visited',
    'after',
    'before',
    'first-letter',
    'first-line',
    'selection',
    # take arguments
    'lang',
    'not',
    'nth-child',
    'nth-last-child',
    'nth-last-of-type',
    'nth-of-type'
]

TAGS = [
    'a',
    'abbr',
    'acronym',
    'address',
    'applet',
    'area',
    'article',
    'aside',
    'audio',
    'b',
    'base',
    'basefont',
    'bdi',
    'bdo',
    'big',
    'blockquote',
    'body',
    'br',
    'button',
    'canvas',
    'caption',
    'center',
    'cite',
    'code',
    'col',
    'colgroup',
    'data',
    'datalist',
    'dd',
    'del',
    'details',
    'dfn',
    'dialog',
    'dir',
    'div',
    'dl',
    'dt',
    'em',
    'embed',
    'fieldset',
    'figcaption',
    'figure',
    'font',
    'footer',
    'form',
    'frame',
    'frameset',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'head',
    'header',
    'hr',
    'html',
    'i',
    'iframe',
    'img',
    'input',
    'ins',
    'kbd',
    'label',
    'legend',
    'li',
    'link',
    'main',
    'map',
    'mark',
    'meta',
    'meter',
    'nav',
    'noframes',
    'noscript',
    'object',
    'ol',
    'optgroup',
    'option',
    'output',
    'p',
    'param',
    'picture',
    'pre',
    'progress',
    'q',
    'rp',
    'rt',
    'ruby',
    's',
    'samp',
    'script',
    'section',
    'select',
    'small',
    'source',
    'span',
    'strike',
    'strong',
    'style',
    'sub',
    'summary',
    'sup',
    'svg',
    'table',
    'tbody',
    'td',
    'template',
    'textarea',
    'tfoot',
    'th',
    'thead',
    'time',
    'title',
    'tr',
    'track',
    'tt',
    'u',
    'ul',
    'var',
    'video',
    'wbr',
]


class ScssLexer(DefaultScssLexer):
    """
    For SCSS stylesheets.
    """

    name = 'SCSS2'
    aliases = ['scss2']
    filenames = ['*.scss']
    mimetypes = ['text/x-scss']

    tokens = {}

    for group, common in iteritems(DefaultScssLexer.tokens):
        tokens[group] = copy.copy(common)

    tokens['root'].insert(5, (r'@if', Keyword, 'if'))
    tokens['root'].insert(6, (r'@else', Keyword, 'else'))
    tokens['root'][9] = (r'(@include)( [\w-]+)', bygroups(Keyword, Name.Function), 'value')
    # tokens['selector'][1] = ('(?=:)', Operator, 'pseudo-class')
    # tokens['selector'].extend([(r'\$[\w-]*\w', Name.Variable)])
    tokens['value'].append((r'\$[\w-]*\w', Name.Variable))
    tokens['if'] = [
        (r'[!%()<>+=-]', Operator),
        include('value'),
        default('#pop')]
    tokens['else'] = [('if', Keyword, 'if'), default('#pop')]
    tokens['pseudo-class'] = [
        (words(PSEUDO_CLASSES, prefix=r':+', suffix=r'\b'), Keyword.Pseudo),
        (r'[()]', Operator),
        include('value'),
        default('#pop')]

    tokens['selector'] = [
        (r'[ \t]+', Text),
        (words(PSEUDO_CLASSES, prefix=r':', suffix=r'\b'), Keyword.Pseudo),
        (words(TAGS, suffix=r'\b'), Keyword),
        (r'\.', Name.Class, 'class'),
        (r'\#', Name.Namespace, 'id'),
        (r'([\w-]+)\s*(:)', bygroups(Name.Attribute, Operator), 'value'),
        (r'[\w-]+', Name.Tag),
        (r'#\{', String.Interpol, 'interpolation'),
        (r'&', Keyword),
        (r'[~^*!&\[\]()<>|+=@:;,./?-]', Operator),
        (r'[{}]', Punctuation),
        (r'"', String.Double, 'string-double'),
        (r"'", String.Single, 'string-single'),
        (r'\$[\w-]*\w', Name.Variable),
    ]
