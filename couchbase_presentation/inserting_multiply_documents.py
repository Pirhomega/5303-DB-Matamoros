# this script will insert a butt-ton of data into a bucket

from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.admin import Admin # the admin class gives me the power to create/delete buckets
from couchbase.n1ql import N1QLQuery

cluster = Cluster('http://127.0.0.1:8091')
authenticator = PasswordAuthenticator('corbinmatamoros', 'MattCorbin')
cluster.authenticate(authenticator)

#open the 'travel-bucket' within the cluster 'cluster'
bucket1 = cluster.open_bucket('class-bucket')

# only has to be run once
# bucket1.n1ql_query('CREATE PRIMARY INDEX ON `class-bucket`').execute()

# the result of the query is stored in the variable 'result'
result = bucket1.n1ql_query('Select * from `class-bucket` where properties.ADMIN = "Armenia"')
for res in result:
    print(res)