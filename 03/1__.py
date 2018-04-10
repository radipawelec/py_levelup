def add_tag(func):
    def decoratedfn(tag):
        return '<'+tag+'>'+'{0}'.format(func(tag))+'</'+tag+'>'
    return decoratedfn


@add_tag
def hello_world(tag):
    return 'Hello world'


print(hello_world('h2'))
