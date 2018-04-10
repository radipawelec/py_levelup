<<<<<<< HEAD
def add_tag(func):
    def prt_func(name):
        return '<p>{0}</p>'.format(func(name))    
    return prt_func


@add_tag
def print_text(name):
    return 'hello,'+ |name

print(print_text('h1'))
=======
def add_tag(msg):
	def decoratored(f):
		print('<'+msg+'>{0}'.format(f()) + '</'+msg+'>')
	return decoratored

@add_tag('h1')
def write_something():
	return 'Hello world'

>>>>>>> 7767ee7f3e212dcd5e9ebb6cdddb580115be78d1
