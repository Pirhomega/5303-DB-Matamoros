date +%s
/Applications/Couchbase\ Server.app/Contents/Resources/couchbase-core/bin/cbimport json -c couchbase://<> -u <> -p <> -b user-connections -d file:///Users/student/Desktop/USER_FRIEND_LIST_MAC.json -f list -g key::%user_id%
date +%s

/Applications/Couchbase\ Server.app/Contents/Resources/couchbase-core/bin/cbimport json -c couchbase://<> -u <> -p <> -b users -d file:///Users/student/Desktop/RandomDataGenerator-master/data.json -f list -g key::%user_id%
date +%s