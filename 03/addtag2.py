def mydecorator(msg):
	def decoratored(f):
		print('<'+msg+'>{0}'.format(f()) + '</'+msg+'>')
	return decoratored

@mydecorator('br')
def hello():
	return 'Hello world'

