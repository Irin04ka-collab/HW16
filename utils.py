import json


def load_data(path):
    """
    функция, которая читает данные из файла
    :param path: путь до файла
    :return: словарь
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# file1 = load_data('data/user.json')
# dict1 = file1[0]
# print(dict1)
# print(dict1.get("last_name"))
#
# new_dict = {}
#
# for name, value in dict1.items():
#     new_dict[name]=value
# print(new_dict)

# list_of_users = load_data('data/user.json')
# dict_result = {}
#
# for item in range(1, len(list_of_users) + 1):
#     print(f"user_{item}={item}")
#
# for user in list_of_users:
#     # dict_result[f"user_{item}"]=
#     print(user)


