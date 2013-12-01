""" Trying and enjoying the single-dispatch_, new in Python3.4.

.. _single-dispatch:: http://www.python.org/dev/peps/pep-0443/
"""

from functools import singledispatch

#######################################
## Creating a `generic function`
#######################################

@singledispatch
def fun(arg):
    return 'default'


## Registering behaviors to correspond to each types


@fun.register(int)
def fun_int(arg):
    return 'int'


@fun.register(list)
def fun_list(arg):
    return 'list'


## Also a class which is not built-in type.


class Model(object):
    pass


@fun.register(Model)
def fun_model(arg):
    return 'model'

## Testing

assert fun(3) == 'int'
assert fun([]) == 'list'
assert fun(Model()) == 'model'

assert fun('str') == 'default'  # str type is not registered.
assert fun(0.0) == 'default'  # fload too.

## Testing redisterd function directoly

assert fun_int('dummy') == 'int'
assert fun_list('dummy') == 'list'
assert fun(object()) == 'default'  # Using 'instance of object' to test the default behavior.

##########################################
## Registering a new fuction by calling
##########################################

fun.register(str, lambda arg: 'str')  # Adding for str type.


assert fun('str') == 'str'  # New behavior was registered correctly.
assert fun(0.0) == 'default'  # float type is not still expected.


##############################
## Trying with child class
##############################

class MemberModel(Model):
    def __init__(self, name):
        self.name = name


assert fun(MemberModel(name='ritsu')) == 'model'  # Yes, it is one of Model.


## Registering a behavior for only the MemberModel.


@fun.register(MemberModel)
def _(arg):
    return 'member: {member.name}'.format(member=arg)


assert fun(MemberModel(name='ritsu')) == 'member: ritsu'


print('Congrats! All tests passed :)')
