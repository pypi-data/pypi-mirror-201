# imports

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import axes
import matplotlib as mpl
from collections import namedtuple, abc
from Reportom import java, html, css
from random import seed, randint

seed()
ids = set()
max_ids = 10000


def create_id():
    c = 0
    i = randint(0, 1000*max_ids)
    while i in ids and c < 1000:
        i = randint(0, 1000*max_ids)
        c += 1
        
    if c < 1000:
        ids.add(i)
        rv = 'F'+hex(i)[2:].upper()
    else:
        rv = None
        print('Ran out of ids!!!')
        raise ValueError
    return rv
        
    
"""
Prototype class that can be used for creating content items
"""
class Content:
    def __init__(self,css_code=None, **kwargs):
        self._type = 'Content'
        self._kwargs = kwargs
        if '_id' not in kwargs.keys():
            self._id = create_id()
            self._kwargs['_id'] = self.ID()
        else:
            self._id = self._kwargs['_id']
        self.css = css.CSS(code=css_code, label='#'+self._id)
        return
    
    def __repr__(self):
        return f'{self._type}(Content)'

    def html(self):
        return f'html is not supported by {self._type}'

    def pdf(self):
        return f'pdf is not supported by {self._type}'

    def ID(self):
        return self._id

    def add_css(self, code):
        #self._css_code.append(str(code))
        self.css.add(code)
        return


class Form(Content):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._type = 'form'
        self._content = []
        return

    def add(self, item):
        self._content.append(item)

    def html(self):
        return html.form('\n'.join(self._content), **self._kwargs)

    def add_from_dict(self,label:str, tag:str, d:dict):
        self.add(
            html.label(html.span(label) + html.short_tag(tag, **d))
        )
        return

    def add_list(self, l):
        for label, tag, config_dict in l:
            self.add_from_dict(label, tag, config_dict)
        return

    def __len__(self):
        return len(self._content)

class Html(Content):

    def __init__(self, html=None, **kwargs):
        super().__init__(**kwargs)
        self._html = str(html)
        self._type = 'Html'
        return

    def html(self):
        return str(self._html)

class Text(Content):
    
    def __init__(self, text=None, **kwargs):
        super().__init__(**kwargs)
        self._text = str(text)
        self._type = 'Text'
        return

    def html(self):
        self._kwargs['_id'] = self._id
        return html.p(self._text, **self._kwargs)


class Image(Content):
    def __init__(self, src=None, **kwargs):
        super().__init__(**kwargs)
        self._type = 'Image'
        self._src = str(src)
        # self._kwargs = kwargs
        
        return

    def html(self):
        return html.img(src=self._src, **self._kwargs)


class Script(Content):
    def __init__(self, code, **kwargs):
        super().__init__(**kwargs)
        self._type = 'Script'
        self._code = str(code)
        # self._kwargs = kwargs
        return
    
    def html(self):
        return html.script(self._code, **self._kwargs)


class MultiImage(Content):
    
    def __init__(self, src: list, prefix: str, image_kwargs: dict = None, **kwargs):
        super().__init__(**kwargs)
        self._type = 'MultiImage'
        # self._kwargs = kwargs
        if isinstance(src, abc.Sequence):
            self._src = list(src)
            self._prefix = str(prefix)
        else:
            print('Expected a sequence like list or tuple etc for src.')
            raise ValueError
        if isinstance(image_kwargs, abc.Mapping):
            self._image_kwargs = dict(image_kwargs)
        elif image_kwargs is None:
            self._image_kwargs = dict()
        else :
            print('expected a dict like parameter for image_kwargs')
            raise ValueError
            
        return

    def add_image(self, src: str):
        self._src.append(src)
        return

    def imagenames(self) -> str:
        return str(self._src)

    def __len__(self):
        return len(self._src)

    def html(self) -> str:
        # create names.
        if len(self) > 0:
            i = self._prefix + 'counter'
            names = self._prefix + 'names'
            Next = self._prefix + 'next'
            Previous = self._prefix + 'Previous'
            image = self._prefix + 'image'
            slider = self._prefix + 'slider'
            jump = self._prefix + 'jump'
            goto = self._prefix + 'goto'
            imagenames = str(self._src)
            j = java.code(f'const {names}={imagenames};')
            j(f'var {i} = 0;')

            # next picture code.
            j.f(Next)
            j(f'{i}++;')
            j.IF(f'{i} >= {names}.length')
            j(f'{i} = 0;')
            j.end() # end if
            j(f'document.getElementById(\'{image}\').src = {names}[{i}];')
            j(f'document.getElementById(\'{slider}\').value = {i};')
            j('return;')
            j.end()  # end function

            # previous picture code.
            j.f(Previous)
            j(f'{i}--;')
            j.IF(f'{i} < 0')
            j(f'{i} = {names}.length - 1;')
            j.end()  # end if
            j(f'document.getElementById(\'{image}\').src = {names}[{i}];')
            j(f'document.getElementById(\'{slider}\').value = {i};')
            j('return;')
            j.end()  # end function

            # jump code
            j.f(jump)
            j(f'{i} = document.getElementById(\'{slider}\').value;')
            j(f'document.getElementById(\'{image}\').src = {names}[{i}];')
            j('return;')
            j.end() # end jump function
            
            #goto code, jump directly to given filename
            j.f(goto, 'i')
            j(f'{i} = i;')
            j(f'document.getElementById(\'{image}\').src = {names}[{i}];')
            j(f'document.getElementById(\'{slider}\').value = {i};')
            j('return;')
            j.end() # end of goto function
            j('\n')

            code = html.script(j, _type='text/javascript') # javaScript code
            img = html.img(src=self._src[0], _id=image, **self._image_kwargs) # the image
            # the controls, 2 buttons and a slider
            buttons = html.table(
                html.tr(
                    html.td(html.button('Previous', onClick=Previous + '()')) +
                    html.td(html.button('Next', onClick=Next + '()')) +
                    html.td(html.input(_id=slider,_type='range', value=0, _min=0, _max=len(self._src)-1, step=1, onmousemove=jump+'()'))
                )
            )
            rv = html.div(code + img + buttons, **self._kwargs)
        else:
            rv = html.div('Empty', **self._kwargs )
        return rv


class MultiPlot(MultiImage):
    def __init__(self, prefix:str, folder=None, w=10, h=10, dpi=300, image_kwargs: dict = None, **kwargs):
        super().__init__([], prefix, image_kwargs=image_kwargs, **kwargs)
        self._dpi = dpi
        self._w = w
        self._h = h
        self._folder = '' if folder is None else str(folder)
        return

    def add_plot(self, ax=None, src=None):
        img = Plot(ax, src, self._folder, w=self._w, h=self._h, dpi=self._dpi).path()
        self.add_image(img)
        return


class Plot(Content):
    # BEWARE src is relative to the html file.
    # folder is to inform the base folder of the report
    def __init__(self, ax=None, src=None, folder=None, w=10, h=10, dpi=300, **kwargs):
        super().__init__(**kwargs)
        self._type = 'Plot'
        self._src = str(src)
        self._dpi = dpi
        # self._kwargs = kwargs
        self._folder = '' if folder is None else str(folder)

        self._ax = ax
        if isinstance(ax, sns.axisgrid.FacetGrid):
            self._fig = ax.figure
        elif isinstance(ax, axes.Axes):
            self._fig = ax.get_figure()
        else:
            print(f'Report.Plot() Expecting either a axes.Axes or FacetGrid type instance! got {type(ax)} instead')
            raise ValueError 
        self._fig.set_figwidth(w)
        self._fig.set_figheight(h)
        if src[0:2] == './' or src[0:2] == '.\\':
            self._filename = self._folder + self._src[2:]
        else:
            self._filename = self._folder + self._src

        self._fig.savefig(self._filename, dpi=dpi)
        plt.clf()        
        return

    def html(self):
        return html.img(src=self._filename, **self._kwargs)

    def path(self):
        return str(self._filename)

# interface object for indivual cell of the table and their html atributes
class TableCell():
    def __init__(self, parent, x,y):
        self._parent = parent
        self._x = x
        self._y = y
        return

    #return value in the table cell
    def value(self):
        return self._parent._df.at[self._x, self._y]

    def attributes(self):
        return self._parent._events.at[self._x, self._y]

    def add_attribute(self,attr, value):
        self.attributes()[attr] = value
        return

# interface object for indivual column of the table and their html atributes
class TableCol():
    def __init__(self, parent, col):
        self._parent = parent
        self._col = str(col)

    #return value in the table cell
    def value(self):
        return self._parent._df[self._col]

    def attributes(self):
        return self._parent._events[self._col]

    def add_attribute(self,attr, value):
        self.attributes().apply(lambda x: x.update({attr:value}))
        return

class Table(Content):
    def __init__(self, df, caption=None, **kwargs):
        super().__init__(**kwargs)
        self._df = df.copy()
        self._events = pd.DataFrame(
            [[{} for x in range(len(df.columns))] for y in range(len(df))],
            index = df.index,
            columns= df.columns
        )
        # self._kwargs = kwargs
        self._type = 'Table'
        if isinstance(caption, str):
            self._caption = str(caption)
        else:
            self._caption = None
        return

    def __len__(self):
        return len(self._df)

    def __getitem__(self,item):
        if isinstance(item,str):
            rv = TableCol(self, item)
        elif isinstance(item,abc.Sequence):
            rv  = TableCell(self, *item)

        return rv

    def html_table_header(self):
        # create a row with table headers
        header = html.th(self._df.index.name) + ''.join([html.th(col) for col in self._df.columns])

        # return it in a table row
        return html.tr(header)

    def html_table_rows(self):
        rows = ''
        # iterate the table rows
        for row in self._df.iterrows():
            # create a single row.
            rows = rows + html.tr(
                html.td(row[0]) + ''.join([html.td(col[1], **self._events.at[row[0], col[0]]) for col in row[1].items()])
            )
                                   
        return rows

    def html(self):
        # create the caption, if available
        if isinstance(self._caption, str):
            caption = html.caption(self._caption)
        else:
            caption = ''
            
        # create the header.
        header = self.html_table_header()
        
        # create the actual table.
        data = self.html_table_rows()
        
        return html.table(caption + header + data, **self._kwargs)
    

"""
Block object, is an object that will holds several text,plot,image,table objects. And will
be displayed a single section or block.
"""
class Block:
    def __init__(self, title='', content=None, logging_enabled=True, _class=None, _id=None, css_code=None):
        # Setup logging
        self._log = []
        self._logging_enabled = logging_enabled
        
        # setup title
        self.set_title(title)

        # setup element type helper
        self._element_type_helper = html.div

        # setup class and id
        self._class = 'block' if _class is None else str(_class)
        self._id = create_id() if _id is None else str(_id)

        # setup initial content
        self._content = list()
        if isinstance(content, Content) or isinstance(content,abc.Sequence):
            self.add_content(content)

        # setup css for block
        self.block_css = css.CSS(code=css_code, label='#'+self._id)

        return
    
    def ID(self):
        return self._id

    def CLASS(self):
        return self._class

    def add_content(self, content):

        if isinstance(content, Content):
            self._content.append(content)
            rv = content
            self.log(f'New content added {content}')
        elif isinstance(content, abc.Sequence):
            rv = []
            for item in content:
                rv.append(self.add_content(item))
        return rv

    def set_title(self, title):
        self._title = str(title)
        self.log(f'Title set: \'{self._title}\'')
        
        return
    
    def log(self, msg):
        if self._logging_enabled:
            self._log.append(str(msg))
        return self._logging_enabled
    
    def __len__(self):
        return len(self._content)

    def __repr__(self):
        return f'Block(title=\'{self._title}\', content={self._content}, logging_enabled={self._logging_enabled}, _class=\'{self._class}\', _id=\'{self._id}\')'

    def html_title(self):
        return html.h1(self._title)

    def html(self):
        content=self.html_title()
        for item in self._content:
            content = content + item.html()
        return self._element_type_helper(content, _class=self._class, _id=self._id)

    def add_css(self, code):
        self.block_css.add(code)
        return

    def css(self) -> str:
        # css code for block it self
        block_code = self.block_css.css()

        # get all css code from the contained contents.
        content_code = '\n'.join( [ c.css() for c in self._content] ) if len(self._content) > 0 else ''

        #return them as one big multiline string
        return  block_code + content_code

    def pdf(self):
        return 'pdf is not supported by block'

    def title(self):
        return str(self._title)

    def add_form(self, **kwargs):
        if '_class' not in kwargs:
            content = Form(_class='form',**kwargs)
        else:
            kwargs['_class'] = kwargs['_class'] + ' form'
            content = Form(**kwargs)
        return self.add_content(content)

    def add_text(self, text, **kwargs):
        if '_class' not in kwargs:
            content = Text(text, _class='text',**kwargs)
        else:
            kwargs['_class'] = kwargs['_class'] + ' text'
            content = Text(text, **kwargs)
        return self.add_content(content)

    def add_html(self, html: str, **kwargs) -> Content:
        return self.add_content( Html(html, **kwargs) )

    def add_image(self, src=None, **kwargs):
        if '_class' not in  kwargs:
            content = Image(src, _class='image',**kwargs)
        else:
            kwargs['_class'] = kwargs['_class'] + ' image'
            content = Image(src, **kwargs)
        return self.add_content(content)

    def add_table(self, df=None, caption=None, **kwargs):
        if '_class' not in  kwargs:
            content = Table(df,caption, _class='table',**kwargs)
        else:
            kwargs['_class'] = kwargs['_class'] + ' table'
            content = Table(df, caption, **kwargs)
        return self.add_content(content)
    
    def add_plot(self, ax=None, src=None, folder=None,**kwargs):
        if '_class' not in  kwargs:
            content = Plot(ax=ax, src=src, folder=folder, _class='plot',**kwargs)
        else:
            kwargs['_class'] = kwargs['_class'] + ' plot'
            content = Plot(ax=ax, src=src, folder=folder, **kwargs)
        return self.add_content(content)

    def add_java(self, code, **kwargs):
        return self.add_content(Script(code, _type='text/javascript', **kwargs))

    def add_multiImage(self, src: list, prefix: str, **kwargs):
        return self.add_content(MultiImage(src, prefix, **kwargs))

    def add_multiPlot(self, *args, **kwargs):
        return self.add_content(MultiPlot(*args, **kwargs))

#
#  HTML 5 section element short cuts for block
#
class Header(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._element_type_helper = html.header
        return

    def html_title(self):
        return ''


class Section(Block):
    def __init__(self, details=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._element_type_helper = html.section
        if details:
            self._element_type_helper = self.html_details
        else:
            self._element_type_helper = html.section
        return

    def html_details(self, content, *arg, **kwargs):
        return html.section(html.details(html.summary(self._title)+ content))

    def html_title(self):
        return ''


class Footer(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._element_type_helper = html.footer
        return
    
    def html_title(self):
        return ''


class Article(Block):
    def __init__(self, details=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if details:
            self._element_type_helper = self.html_details
        else:
            self._element_type_helper = html.article
        return

    def html_details(self, content, *arg, **kwargs):
        return html.article(html.details(html.summary(self._title)+ content))

    def html_title(self):
        return ''

class Nav(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._element_type_helper = html.nav
        return

"""
Main Page Object used to create, maintain and save a html page.
"""
class Page:
    def __init__(self, title='', blocks=None, logging_enabled=True, folder=None,html_file=None,css_file=None, lang='en', encoding='utf-8'):
        # Setup logging
        self._log = []
        self._logging_enabled = logging_enabled
        
        # setup title
        self.set_title(title)

        #language
        self._lang=lang

        # setup filenames
        self._encoding=encoding
        self._folder_name = str(folder) if isinstance(folder,str) else './'
        self._html_file = self._folder_name + str(html_file) if isinstance(html_file,str) else self._folder_name + 'report.html'
        self._css_file = self._folder_name + str(css_file) if isinstance(css_file,str) else None

        # setup any initials blocks
        self._blocks = list()
        if isinstance(blocks, Block) or isinstance(blocks, abc.Sequence):
            self.add_block(blocks)

        # setup CSS
        self._css_code = []

        return

    def set_title(self,title):
        self._title = str(title)
        self.log(f'Title set: \'{self._title}\'')
        return

    def log(self,msg):
        if self._logging_enabled:
            self._log.append(str(msg))
        return self._logging_enabled

    def __len__(self):
        return len(self._blocks)

    def __repr__(self):
        return f'Report(title=\'{self._title}\', blocks={self._blocks}, logging_enabled={self._logging_enabled}, html_file=\'{self._html_file}\', css_file=\'{self._css_file}\')'

    def add_block(self, block=None, **kwargs):
        rv = True
        if block is None:
            self.add_block(Block(**kwargs))
        elif isinstance(block, Block):
            self._blocks.append(block)
            self.log(f'Added new block: {block.title()}')
        elif isinstance(block,abc.Sequence):
            for item in block:
                self.add_block(item)
        return self._blocks[-1]

    def add_css(self, code, label='body'):
        if isinstance(code, css.CSS): # if its an CSS object -> turn into CSS code sting and add.
            self._css_code.append(code())
        elif isinstance(code, str) or isinstance(code, css.Style):   # if its a string or Style object, just copy and add.
            self._css_code.append(str(code))
        elif isinstance(code, abc.Mapping): # if its a dict, use the label parameter to create a css object to convert into string and add
            self.add_css( css.CSS(code=code, label=label))
        elif isinstance(code, abc.Sequence): # if its a list, iterate and add contents of the list.
            for item in code:
                self.add_css(item)
        return
    
    def htmlheader(self):
        # if we have a file name specified for the CSS code we will insert a link for it in the header
        # if not the we will put the css code in the the header
        if isinstance(self._css_file, str):
            header = html.link(rel='stylesheet', href=self._css_file)
        else:
            header = html.style(self.css())
        header = html.title(self._title) + header # add a title
        header = html.meta( charset=self._encoding) + header # write endcoding type
        return html.head( header )
    
    def html(self):
        header = self.htmlheader()
        blocks = ''
        for block in self._blocks:
            blocks = blocks + block.html()
        code = html.html(header + html.body(blocks), lang=self._lang)
        return html.make_readable(code)

    def pdf(self):
        return ''

    def title(self):
        return str(self._title)
    
    def css(self):
        code_list = self._css_code
        for block in self._blocks:
            for css in block.css():
                code_list.append(css)
        code  =''.join( code_list )
        
        return code

    def save(self):
        # write the html file.
        file = open(self._html_file, 'wt', encoding=self._encoding)
        file.write(self.html())
        file.close()
        
        # if we jave a css file specified we will write it.
        if isinstance(self._css_file, str):
            file = open(self._css_file, 'wt', encoding=self._encoding)
            file.write(self.css())
            file.close()
        return

