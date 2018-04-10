sent_json = {"first_name": "James", "last_name": "Bond", 'age':'12'}


def validate_json(*json_arguments, **kwargs):
    def decorated(f):
        result = f()
        for i in result:
            if i not in json_arguments:
                raise ValueError
        return 'ok'
    return decorated


@validate_json('first_name', 'last_name', 'age')
def process_json():
    return sent_json

print(process_json)