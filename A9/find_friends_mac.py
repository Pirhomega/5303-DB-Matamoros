import json
import random

# open input file and load data into json_list_users
with open("/Users/student/Downloads/5303-DB-Matamoros-master/A9/USERS_LIST.json", "r") as file:
    json_list_users = json.load(file)

friend_list = []

for count1 in range(0,10000):
    friend_count = random.randint(1, 338)
    friend_list.append({"user_id": count1, "friend_count" : friend_count, "friends" : []})
    for count2 in range(0,friend_count):
        friend_list[count1]["friends"].append(random.randint(0,10000))

# write new data to output file
with open("/Users/student/Downloads/5303-DB-Matamoros-master/A9/USER_FRIEND_LIST_MAC.json", 'w') as write_file:
    json.dump(friend_list, write_file)