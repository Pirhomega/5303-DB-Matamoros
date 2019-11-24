What I did:
	1. Downloaded 10 files of 1000 users from mockaroo, compiled them into one document.
	2. Created a short script that replaced "user_id" field with a number of 0-9999 (pretty_json.py)
	3. Uploaded users to users bucket (cbimport json -c couchbase://127.0.0.1 -u corbinmatamoros -p MattCorbin -b users -d file:///Users/Owner/Desktop/5303-DB-Matamoros/A9/USERS_LIST.json -f list -g key::%user_id%)
    4. Created a primary index on bucket `users` (```sql create primary index `users-primary-index` on `users````)
    5. Created a short script to generate friends for each user (find_friends.py)
    6. Upload user_friends to user_connections bucket (cbimport json -c couchbase://127.0.0.1 -u corbinmatamoros -p MattCorbin -b user-connections -d file:///Users/Owner/Desktop/5303-DB-Matamoros/A9/USER_FRIEND_LIST.json -f list -g key::%user_id%)
    7. Created a primary index on bucket `user_connections` (create primary index `user-connections-primary-index` on `user-connections`)