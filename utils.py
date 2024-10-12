import json


def load_data(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# file1 = load_data('data/user.json')
# print(type(file1))