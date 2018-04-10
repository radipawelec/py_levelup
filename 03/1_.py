def add_tag(sentence):
    def real_decorator(to_be_decorated):
        def wrapper(*args, **kwargs):
            result = to_be_decorated(*args, **kwargs)
            return f'<{sentence}>{result}</{sentence}>'
        return wrapper
    return real_decorator
 
@add_tag('h1')
def write_something():
    return 'something'
 
result = write_something()
assert result == '<h1>something</h1>'