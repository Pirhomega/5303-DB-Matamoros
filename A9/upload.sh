# we use 'date +%s' to track instruction execution time
date +%s
/Applications/Couchbase\ Server.app/Contents/Resources/couchbase-core/bin/cbimport json -c couchbase://<cluster ip> -u <username> -p <password> -b user-connections -d file:///Users/student/Desktop/USER_FRIEND_LIST_MAC.json -f list -g key::%user_id%
date +%s

/Applications/Couchbase\ Server.app/Contents/Resources/couchbase-core/bin/cbimport json -c couchbase://<cluster ip> -u <username> -p <password> -b users -d file:///Users/student/Desktop/RandomDataGenerator-master/data.json -f list -g key::%user_id%
date +%s