import json


data_db = [
    {
        "resource": 'Github',
        "login": 'login',
        "password": 'cn8ev78ewv'
        }
    ]

json_str = """
[
    {
        "resource": "Github",
        "login": "oop0022"
    },
    {
        "resource": "w",
        "login": "2222"
    },
    {
        "resource": "e",
        "year": "3333"
    }
]"""

items = json.loads(json_str)
item = items[0]

print(item['resource'], item['login'])

#
# with open("data_file.json", "r") as read_file:
#     data = json.load(read_file)
#     print(data)
#
# with open("data_file.json", "w") as write_file:
#     json.dump(data, write_file, indent=4)
