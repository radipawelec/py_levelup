sent_json = {"first_name": "James", "last_name": "Bond", 'age':'12'}


def mydecorator(*json_arguments, **kwargs):
    def decorated(f):
        result = f()
        for i in result:
            if i not in json_arguments:
                raise ValueError
        return len(result)
    return decorated


@mydecorator('first_name', 'last_name', 'age')
def hello():
    return sent_json

print(hello)