# script will unload a json file of 1,000,000 documents/users
# and, per user, assign a list of users to act as friends. Then it
# will dump the newly created data into a json file

import json
import random

# open input file and load data into json_list_users
with open("C:/Users/Owner/Desktop/5303-DB-Matamoros/A9/USERS_LIST.json", "r") as file:
    json_list_users = json.load(file)

friend_list = []

# loop through all one-million users, randomly assigning a number of friends to each
for count1 in range(0,10000):
    friend_count = random.randint(1, 338)
    friend_list.append({"user_id": count1, "friend_count" : friend_count, "friends" : []})
    # populate the friend list with 'friend_count' number of users randomly
    for count2 in range(0,friend_count):
        friend_list[count1]["friends"].append(random.randint(0,10000))

# write new data to output file as json file type
with open("C:/Users/Owner/Desktop/5303-DB-Matamoros/A9/USER_FRIEND_LIST.json", 'w') as write_file:
    json.dump(friend_list, write_file)