import json
import random
from hashlib import sha256


def write_code(username):
    obj = read_codes()
    random_number = random.randint(10000000, 99999999)
    while random_number in obj.values():
        random_number = random.randint(10000000, 99999999)
    obj[username] = sha256(str(random_number).encode('utf-8')).hexdigest()
    with open("sample.json", "w") as outfile:
        json.dump(obj, outfile)


def read_codes():
    with open('sample.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        print(json_object)
        print(type(json_object))
        return json_object

write_code("ARNOLD612")
read_codes()