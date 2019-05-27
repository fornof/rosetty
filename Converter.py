# from pygments import highlight
# from pygments.lexers import get_lexer_by_name
# from pygments.formatters import HtmlFormatter
# code = 'print "Hello World"'
# lexer = get_lexer_by_name("python", stripall=True)
# formatter = HtmlFormatter(linenos=True, cssclass="source")
# result = highlight(code, lexer, formatter)
#print(result)
import markdown
import yaml 
import yamlordereddictloader
import sys

# -*- coding: utf-8 -*-
"""
    The Pygments Markdown Preprocessor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This fragment is a Markdown_ preprocessor that renders source code
    to HTML via Pygments.  To use it, invoke Markdown like so::

        import markdown

        html = markdown.markdown(someText, extensions=[CodeBlockExtension()])

    This uses CSS classes by default, so use
    ``pygmentize -S <some style> -f html > pygments.css``
    to create a stylesheet to be added to the website.

    You can then highlight source code in your markdown markup::

        [sourcecode:lexer]
        some code
        [/sourcecode]

    .. _Markdown: https://pypi.python.org/pypi/Markdown

    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

# Options
# ~~~~~~~

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = False


import re

from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
import yaml

class CodeBlockPreprocessor(Preprocessor):

    pattern = re.compile(r'\[sourcecode:(.+?)\](.+?)\[/sourcecode\]', re.S)

    formatter = HtmlFormatter(noclasses=INLINESTYLES)

    def run(self, lines):
        def repl(m):
            try:
                lexer = get_lexer_by_name(m.group(1))
                #lexer = get_lexer_by_name("python", stripall=True)
            except ValueError:
                lexer = TextLexer()
            code = highlight(m.group(2), lexer, self.formatter)
            code = code.replace('\n\n', '\n&nbsp;\n').replace('\n', '<br />')
            return '\n\n<div class="code">%s</div>\n\n' % code
        joined_lines = "\n".join(lines)
        joined_lines = self.pattern.sub(repl, joined_lines)
        return joined_lines.split("\n")

class CodeBlockExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        #deprecated , use register instead
        md.preprocessors.add('CodeBlockPreprocessor', CodeBlockPreprocessor(), '_begin')
def add_line_breaks( string,width=100):
    char_count = 0
    index = 0;
    last_space = 0
    comment_line = False
    py_comment_line = False
    line_breaker = "\n\t"
    for char in string:
        if char =='#':
            py_comment_line = True
        elif char == '/':
            if string[index+1] == '/':
                comment_line = True
        elif char == '\n':
            char_count = 0 
            comment_line = False
            py_comment_line = False
        elif char == ' ':
            last_space = index
        else:
            char_count +=1
        if char_count >= width:
           string= string[0:last_space] + line_breaker+ comment_line*'//'+py_comment_line*"#" + string[last_space:]
           char_count = 0
        index +=1
    return string 

def process(highlight_string):
    
    # someText= ''' 
    # [sourcecode:python]
    # def foo(stuff):
    #     print("hello world")
    #     print("hi")
    # [/sourcecode]'''
    highlight_string = add_line_breaks(width=55, string = highlight_string)
    html = markdown.markdown(highlight_string, extensions=[CodeBlockExtension()])
    print(html)
    return html
def writeYaml(data, name="public/rendered-sections.yaml"):
    yaml.dump(
    data,
    open(name, 'w'),
    Dumper=yamlordereddictloader.Dumper,
    default_flow_style=False,explicit_start=True)

def readYaml():
    file = sys.argv[1]
    data = yaml.load(open(file),Loader=yamlordereddictloader.Loader)
    #import pdb;pdb.set_trace()
    #data['languages'][1]['sections'][1].keys()
    languages = data['languages']
    for language in languages:
        if language =='global':
            continue
        sections= language['sections']
        for section in sections:
            for key, value in section.items():
                if key == "instructions":
                     continue # no formatting on the instructions, that is all manual
                if key == "title":
                    continue # no formatting on the title, that is all manual
                if type(value) == type([]):
                    section[key] =[process(value[0])]
                else:
                    section[key] = process(value)
    writeYaml(data)

readYaml() 



