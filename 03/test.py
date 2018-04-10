
sent_json = {"first_name": "James", "last_name": "Bond"}

def mydecorator(*args):
	def decoratored(f):
		if args in '{0} '.format(f()):
			return len(sent_json)
		else:
			return ValueError('could not find')
	return decoratored

@mydecorator('first_name', 'last_name', 'third_name')
def hello():
	return sent_json

print(hello)

