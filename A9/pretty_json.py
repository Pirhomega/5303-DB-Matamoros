# this program will renumber the "user_id" field from 0 to N
# Thank you, https://realpython.com/python-json/#python-supports-json-natively
import json

# open input file and load data into json_list_users
with open("C:/Users/Owner/Desktop/messages_data/shit-ton-of-data/MOCK_DATA-0.json", "r") as file:
    json_list_users = json.load(file)

# list that'll hold new json data
NEW_DATA = []

id = 0

# loop through each document in json_list_users, renumber user_id, and append to NEW_DATA
for user in json_list_users:
    user["user_id"] = id
    NEW_DATA.append(user)
    id+=1

# write new data to output file
with open("C:/Users/Owner/Desktop/messages_data/shit-ton-of-data/USERS_LIST.json", 'w') as write_file:
    json.dump(NEW_DATA, write_file)