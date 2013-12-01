from functools import singledispatch


###############################
## Provided by libraries
###############################


class Message(object):
    """ Messages to communicate each robots.
    """
    def __init__(self, body, **metadata):
        self.body = body
        self.metadata = metadata

    def __str__(self):
        return '''\
{self.body}
* metadata: {self.metadata}
'''.format(self=self)


@singledispatch
def generate_message(arg):
    """ Creating Message object for each types.
    """
    raise TypeError('Unexpected type')


@generate_message.register(str)
def str_to_message(arg):
    return Message(arg)


@generate_message.register(dict)
def dict_to_message(arg):
    body = arg.pop('body')
    return Message(body, **arg)


def as_robot(func):
    def wrapped(*args, **kwargs):
        ret = func(*args, **kwargs)
        return generate_message(ret)
    return wrapped


###########################
## Provided by users
###########################


@as_robot
def antique(message):
    return "Good morning, Master Ren."


@as_robot
def neomodel(message):
    return {'body': "I'm here.",
            'enjoyment': 1}


@as_robot
def warrior(message):
    return ['Yes, sir!']


if __name__ == '__main__':
    print('antique::', end=' ')
    print(antique('dummy message'))
    print('neomodel::', end=' ')
    print(neomodel('dummy message'))

    # Adding a new message handler on runtime.
    generate_message.register(list, lambda arg: Message(arg[0]))

    print('warrior::', end=' ')
    print(warrior('dummy message'))
