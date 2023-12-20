
import os, sys
from typing import List

'''
another docstring
example:
-----
> yeas
\n
'''
CONSTANT_THING = int(1.234)
dict_ = {
    "df":f"{CONSTANT_THING}",
}
x  =sum([1,2])
y = 2+1*123
if x == y:
    if x<=y:
        while x >= y:
            print('something')
# a comment
def a_func(thing:int=5,anotherthing:List[int]=[5,6,7]):
    if thing != anotherthing:
        return thing
    elif True and 6:
        raise ValueError 
    else: 
        return False
class MyClass:
    '''
    Some Class docstring
    '''
    def __init__(self, x, *args) -> None:
        self.x = dict(x=3)
        self.att = 1.6
    def __add__(self, other):
        return sum([self.x['x'], other])
    def fun(self, functin):
        return (x for x in range(10))
    
para = 6
a_func(5, [para])
c = MyClass(x=13,)
a = 'x'
c.x[a] = 12
li = [1,2,4/5,53,12]
z = [[[[[[[[[[[[[[[[[1]]]]]]]]]]]]]]]]]
def f(ham: str, eggs: str = 'eggs') -> str:
    print("Annotations:",\
           f.__annotations__)
    print("Arguments\n:", ham, eggs)
    return ham + ' and ' + eggs
unpackes = [*(x for x in range(10))]
m = MyClass(x=1)
strin = '{x.:2f}%'
f(,)
x[1:2]
print(x, 2)\
def x():
    ...
    pass
x = 1

