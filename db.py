import json
from enc_obs import enc_data, dec_data


password = 'password'
__enc__ = enc_data('secure_data', password)

file_dat = 'enc_data.dat'
file_csv = 'enc_data.csv'

json_str = [
    {
        "resource": enc_data('Github', password),
        "login": enc_data('login', password),
        "password": enc_data('password', password)
    },
    {
        "resource": "w",
        "login": "2222"
    },
    {
        "resource": "e",
        "year": "3333"
    }
]

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
