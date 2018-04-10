import json
from pprint import pprint

def validate_json(sentence1, sentence2):
    def real_decorator(to_be_decorated):
        def wrapper(*args, **kwargs):
            result = args[0]
            data = json.loads(result)
            try:
                if sentence1 in data and sentence2 in data and result.count(':') == 2:
                    return to_be_decorated(*args, **kwargs)
                else:
                    raise ValueError
            except ValueError:
                print("o nie ValueError!")
        return wrapper
    return real_decorator
 
@validate_json('first_name', 'last_name')
def process_json(json_data):
    return len(json_data)
 
result = process_json('{"first_name": "James", "last_name": "Bond"}')
assert result == 44


process_json()