from collections import namedtuple, OrderedDict

#create a workspace tuple
Mask = namedtuple('Mask', 'start end on')

#Create a tuple holding our readability styling settings.
Styling = namedtuple('Styling', 'indent single_line max_width newline indent_char escape encoding')
styling = Styling(
    ['DIV', 'HTML', 'HEAD', 'TR', 'TABLE'], # new line and increase indent.
    ['LINK', 'P'], # only new line after statement closes.
    80,# maximum number of carracters on a single line, if single_line or no_action, we will inser a new line after so many carracters
    '\n', # newline caracter
    '  ', # string that we insert as indentation
    ['\'', '\"'], #within these caracters nothing should be changed
    'utf-8' #enconding to use
    )

"""
Short code form tag creating functions
"""
def style(content, **kwargs):
    return tag('STYLE', content, **kwargs)

def button(content, **kwargs):
    return tag('BUTTON', content, **kwargs)

def div(content, **kwargs):
    return tag('DIV', content, **kwargs)

def fieldset(content, **kwargs):
    return tag('FIELDSET', content, **kwargs)

def script(content, **kwargs):
    return tag('SCRIPT', content, **kwargs)

def html(content, **kwargs):
    return '<!DOCTYPE html>\n' + tag('HTML', content, **kwargs)

def header(content, **kwargs):
    return tag('HEADER', content, **kwargs)

def section(content, **kwargs):
    return tag('SECTION', content, **kwargs)

def footer(content, **kwargs):
    return tag('FOOTER', content, **kwargs)

def article(content, **kwargs):
    return tag('ARTICLE', content, **kwargs)

def nav(content, **kwargs):
    return tag('NAV', content, **kwargs)

def title(content, **kwargs):
    return tag('TITLE', content, **kwargs)

def table(content, **kwargs):
    return tag('TABLE', content, **kwargs)

def caption(content, **kwargs):
    return tag('CAPTION', content, **kwargs)

def tr(content, **kwargs):
    return tag('TR', content, **kwargs)

def p(content, **kwargs):
    return tag('P', content, **kwargs)

def details(content, **kwargs):
    return tag('DETAILS', content, **kwargs)

def summary(content, **kwargs):
    return tag('SUMMARY', content, **kwargs)

def label(content, **kwargs):
    return tag('LABEL', content, **kwargs)

def strong(content, **kwargs):
    return tag('STRONG', content, **kwargs)

def b(content, **kwargs):
    return tag('B', content, **kwargs)

def i(content, **kwargs):
    return tag('I', content, **kwargs)

def span(content, **kwargs):
    return tag('SPAN', content, **kwargs)

def form(content, **kwargs):
    return tag('FORM', content, **kwargs)

def datalist(content, **kwargs):
    return tag('DATALIST', content, **kwargs)

def option(content, **kwargs):
    return tag('OPTION', content, **kwargs)

def legend(content, **kwargs):
    return tag('LEGEND', content, **kwargs)

def h1(content, **kwargs):
    return tag('H1', content, **kwargs)

def h2(content, **kwargs):
    return tag('H2', content, **kwargs)

def h3(content, **kwargs):
    return tag('H3', content, **kwargs)

def h4(content, **kwargs):
    return tag('H4', content, **kwargs)

def h5(content, **kwargs):
    return tag('H5', content, **kwargs)

def h6(content, **kwargs):
    return tag('H6', content, **kwargs)

def ul(content, **kwargs):
    return tag('UL', content, **kwargs)

def li(content, **kwargs):
    return tag('LI', content, **kwargs)

def ol(content, **kwargs):
    return tag('OL', content, **kwargs)

def th(content, **kwargs):
    return tag('TH', content, **kwargs)

def td(content, **kwargs):
    return tag('TD', content, **kwargs)

def body(content, **kwargs):
    return tag('BODY', content, **kwargs)

def head(content, **kwargs):
    return tag('HEAD', content, **kwargs)

def img(**kwargs):
    return short_tag('IMG', **kwargs)

def meta(**kwargs):
    return short_tag('META', **kwargs)

def a(content, **kwargs):
    return tag('A',content, **kwargs)

def input(**kwargs):
    return short_tag('INPUT', **kwargs)

def link(**kwargs):
    return short_tag('LINK', **kwargs)

"""
Root tag creating functions
"""
def create_attribute_string(**kwargs) -> str:
    """
    Turns all keyword arguments into to one attribute string for html elements.
    remove leading '_' from property names.
    replaces all other '_' for '-'
    example

        create_attribute_string(_id='dude', _class='mule', data_backpack='123sdfjskjf', required=None)

    returns:

        'id="dude" class="mule" data-backpack="123sdfjskjf" required'

    """
    content = ''
    for key in kwargs:
        attribute = key.lstrip('_')
        if kwargs[key] is None:
            content = content + f' {attribute}'
        else:
            content = content + f' {attribute}=\"{kwargs[key]}\"'
    return content


def tag(tag, fill,**kwargs):
    return f'<{tag}{create_attribute_string(**kwargs)}>{fill}</{tag}>'


def short_tag(tag, **kwargs):
    return f'<{tag}{create_attribute_string(**kwargs)}>'

"""
HTML passing code.
"""
#transform flat HTML to human readable. By indenting and adding new lines. According to styling.
def make_readable(original):
    #discover the layout of the data
    return original


