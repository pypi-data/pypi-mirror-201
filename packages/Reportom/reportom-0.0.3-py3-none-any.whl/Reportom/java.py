# some simple stuff to make producing java code within python a bit easier.
from collections import OrderedDict


# insert a piece of code within hooks.

def hks(code: str) -> str:
    return '{' + code + '}'

# produce and if statement
def IF(condition: str, code: str) -> str:
    return f'if ({condition})' + hks(code)

# produce an if else statement
def IF_ELSE(condition: str, code: str, elseCode: str) -> str:
    return f'if ({condition})' + hks(code) + ' else ' + hks(elseCode)

# produce a switch statement
def switch(expression: str, case_code: OrderedDict) -> str:
    cases = [f'case {case}:\n{case_code[case]} break;\n' for case in case_code]

    return f'switch ({expression})' + hks(''.join(cases))


# return function with given name and code.
def function(name: str, code: str) -> str:
    return f'function {name}()' + hks(code)

# code object can be use to construct a piece of javascript code using its different methods.
# Or even just by calling the object itself.
# The actual javascript code will be produced upon converion to str.
# like:
# myCode = code()
# myCode('let x = 0')
# myCode.IF('x < 10 ')
# myCode('i++')
# myCode.ELSE()
# myCode('i = 0')
# myCode.End()
# myCode.End()
# print(str(myCode))

class code():
    def __init__(self, code: str):
        self._code = [str(code)]
        self._index = 0
        return

    def __str__(self):
        return '\n'.join(self._code)

    def __repr__(self):
        return '\n'.join(self._code)

    # add a line of code.
    def add(self, code: str):
        indent = ('  '.join(['' for i in range(self._index + 1)]))
        self._code.append(indent + str(code))
        return

    def __call__(self, code: str):
        self.add(code)
        return self

    # indent.
    def out(self):
        self._index = self._index + 1
        return
    # indent back.
    def back(self):
        self._index = self._index - 1
        return

    # start coding function x
    def f(self, name, *params):
        param_def = str(list(params))[1:-1].replace('\'', '')
        self.add(f'function {name}({param_def})' + r' {')
        self.out()
        return self

    # start and if block
    def IF(self, condition):
        self.add(r'if (' + condition + r'){')
        self.out()
        return self

    # start and else block
    def ELSE(self):
        self.add(r'} else {')
        self.back()
        self.out()
        return self

    # close a block
    def end(self):
        self.back()
        self.add(r'}')
        return self
