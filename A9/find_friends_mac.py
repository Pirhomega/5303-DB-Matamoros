# script will unload a json file of 1,000,000 documents/users
# and, per user, assign a list of users to act as friends. Then it
# will dump the newly created data into a json file

import json
import random
from datetime import datetime
import time

# open input file and load data into json_list_users
with open("/Users/student/Desktop/RandomDataGenerator-master/data.json", "r") as file:
    json_list_users = json.load(file)

friend_list = []

# use 'start' to measure execution time of the program
start = time.perf_counter()

# loop through all one-million users, randomly assigning a number of friends to each
for count1 in range(1,1000001):
    friend_count = random.randint(1, 338)
    friend_list.append({"user_id": count1, "friend_count" : friend_count, "friends" : []})
    if (count1 % 10000 == 0):
        print(str(count1) + " completed!")
    # populate the friend list with 'friend_count' number of users randomly
    for count2 in range(0,friend_count):
        friend_list[count1-1]["friends"].append(random.randint(1,1000001))

# write new data to output file as json file type
with open("/Users/student/Desktop/USER_FRIEND_LIST_MAC.json", 'w') as write_file:
    json.dump(friend_list, write_file)
execution_time = time.perf_counter() - start
print(execution_time)