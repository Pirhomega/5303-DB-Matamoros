import json
import random
from datetime import datetime
import time

# open input file and load data into json_list_users
with open("/Users/student/Desktop/RandomDataGenerator-master/data.json", "r") as file:
    json_list_users = json.load(file)

friend_list = []
start = time.perf_counter()
for count1 in range(1,1000001):
    friend_count = random.randint(1, 338)
    friend_list.append({"user_id": count1, "friend_count" : friend_count, "friends" : []})
    if (count1 % 10000 == 0):
        print(str(count1) + " completed!")
    for count2 in range(0,friend_count):
        friend_list[count1-1]["friends"].append(random.randint(1,1000001))

# write new data to output file
with open("/Users/student/Desktop/USER_FRIEND_LIST_MAC.json", 'w') as write_file:
    json.dump(friend_list, write_file)
execution_time = time.perf_counter() - start
print(execution_time)