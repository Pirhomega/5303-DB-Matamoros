# What I did to complete this project on Windows:
1. Downloaded 10 files of 1000 users from mockaroo, compiled them into one document.
2. Created a short script that replaced "user_id" field with a number of 0-N (pretty_json.py)
3. Uploaded users to users bucket (cbimport json -c couchbase://127.0.0.1 -u <> -p <> -b users -d file:///Users/Owner/Desktop/5303-DB-Matamoros/A9/USERS_LIST.json -f list -g key::%user_id%)
4. Created a primary index on bucket `users` (```sql create primary index `users-primary-index` on `users````)
5. Created a short script to generate friends for each user (find_friends.py)
6. Upload user_friends to user_connections bucket (cbimport json -c couchbase://127.0.0.1 -u <> -p <> -b user-connections -d file:///Users/Owner/Desktop/5303-DB-Matamoros/A9/USER_FRIEND_LIST.json -f list -g key::%user_id%)
7. Created a primary index on bucket `user_connections` (create primary index `user-connections-primary-index` on `user-connections`)
8. Created script that uploads a message to a bucket
# What I did to complete this project on Mac:
1. Used (https://github.com/BenDiekhoff/RandomDataGenerator) to generate a json file of 1,000,000 documents/users
2. Used 'find_friends-mac.py' to create friends for each of the 1,000,000 users and dumped result into another json file
3. Uploaded both json files to the couchbase instance using 'upload.sh'. The first json file took 126s to upload. The second json file took 112s.
4. Prepared the computer for message uploading by running 'couch.sh'
5. Prepared the couchbase buckets for quicker querying by assigning primary indexes and standard indexes. Primary indexes were created on all four buckets on a field that is 100%
    unique amongst all 1,000,000 users. Standard indexes were created on fields that were used in querying in 'upload_message_mac.py' (see 'indexes.png')
6. Ran 'upload_message_mac.py' on all computers to simulate a chat service uploading messages sent between users to Couchbase.