# css.py
# helper functions for css code
#
from collections import abc,defaultdict
# return a string, code within curly brackets.
def hks(code: str) -> str:
    return '{\n' + code + '}\n'

# create a css block for given label, from code lines in list
def from_list(label: str, code: list) -> str:
    return label + ' ' + hks('\n'.join(code) )

# create a css block for given label, from given dict
def from_dict(label:str, d: dict):
    return from_list(label, [ f'{key}: ' + ' '.join(d[key]) + ';' for key in d])

#given a list of css lines. it will return a block adressed to the given _id
def id_block(_id: str, code: list) -> str:
    return from_list('#'+_id, code)

# object to help create and manage CSS code.
# code can be supplied in dict, string and list form.
# also other CSS object can be supplied as a input source.
# eiter at construction with the code label or afterwards with the .add() method.
# the label label can be used during construction to specify the label for that the css code ill be linked to.
# it is possible to add two CSS objects like: c = a + b . After this C will have the combined code of a and b. But no label
# a new label can be set with .set_label() method.
# use .css() or call the object it self to get the actual CSS code.
class CSS():
    def __init__(self, code=None, label=None):
        self._label = '' if label is None else str(label)
        self._data = dict()
        if code is not None:
            self.add(code)
        return

    def set_label(self, label):
        self._label = str(label)
        return

    def label(self):
        return str(self._label)

    # add new or modify code
    def add(self, code):
        # do we have a plain string?
        if isinstance(code, str):
            self.add_from_string(code)
        # do we have a dictionary?
        elif isinstance(code, abc.Mapping):
            self.add_from_dict(code)
        # do we have another CSS object
        elif isinstance(code, CSS):
            self.add_from_dict(code.as_dict())
        # do we have a list stuff?
        elif isinstance(code, abc.Sequence):
            self.from_list(code)
        else:
            print('Expected str, list or dict')
            raise ValueError
        return

    # given a string with css code, it will add it to the _data dictionary
    def add_from_string(self, code):
        for statement in code.split(';'):
            if len(statement) > 0:
                key, value = statement.split(':')
                self._data[key.strip(' ')] = tuple(value.strip(' ').split(' '))
        return

    # given a dict of option : setting it will add them to the current _data dictionary.
    # Its smart enough to deal with mixed format between str and tuple.
    def add_from_dict(self, d):
        for key in d:
            item = d[key]
            if isinstance(item, str):
                self._data[key] = tuple(item.strip(' ').split(' '))
            elif isinstance(item, abc.Sequence):
                self._data[key] = tuple(item)
            else:
                print('Expected str or dict')
                raise ValueError
        return

    # given a list of strings, all will be added to the ._data dictionary
    def from_list(self, seq):
        for item in seq:
            self.add_from_string(item)
        return

    def as_dict(self):
        return dict(self._data)

    def css(self):
        rv = from_dict(self._label, self._data) if len(self) > 0 else ''
        return rv

    def __call__(self):
        return self.css()

    def __repr__(self):
        return f'CSS({self.as_dict()}, label=\'{self._label}\')'

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, item, value):
        self.add_from_dict({item:value})
        return

    def __add__(self, other):
        rv = CSS(code=self.as_dict())
        rv.add(other.as_dict())
        return rv

    def __str__(self)->str:
        return self.css()

# Style class.
# The Style class will hold multiple CSS objects. Basicaly to provide a interface for managing a complete style set.
class Style():
    def __init__(self):
        self.css_set = dict()
        return

    def __repr__(self):
        return 'Style()'

    def __str__(self):
        return self.css()
    
    def __len__(self):
        return len(self.css_set)

    def __setitem__(self, key, value):
        if len(key) == 2:
            self.set(key[0], key[1],value)
        elif len(key) == 1:
            self.set_dict(key[0], value) 
        else:
            raise IndexError
        return
    
    def __getitem__(self, key):
        if len(key) != 2:
            raise IndexError
        return self.css_set[key[0]][key[1]]

    def css(self):
        code_list = [str(self.css_set[element]) for element in self.css_set]
        return ''.join(code_list)
    
    # set a value for the style.
    def set(self, element, option, value):
        if element in self.css_set:
            # The element exists, so we can modify it.
            self.css_set[element][option] = value
        else:
            # We will create a new CSS() object for it.
            self.css_set[element] = CSS(code={option:value},label=element)
        return
    
    def set_dict(self, element, value):
        self.css_set[element].add(value)