# this script will insert a butt-ton of data into a bucket
# PYTHON 3.8 DOES NOT SUPPORT COUCHBASE PYTHON SDK

from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.admin import Admin # the admin class gives me the power to create/delete buckets
from couchbase.n1ql import N1QLQuery

cluster = Cluster('http://127.0.0.1:8091')
authenticator = PasswordAuthenticator('corbinmatamoros', 'MattCorbin')
cluster.authenticate(authenticator)

#open the 'class-bucket' within the cluster 'cluster'
bucket1 = cluster.open_bucket('class-bucket')

# only has to be run once
# bucket1.n1ql_query('CREATE PRIMARY INDEX ON `class-bucket`').execute()

# the result of the query is stored in the variable 'result'
# result = bucket1.n1ql_query('Select * from `class-bucket` where properties.ADMIN = "Armenia"')
# for res in result:
#     print(res)

# will update all documents with 'geometry.type' = "MultiPolygon" with 'version = "1.0.1"'
"""As a convenience for queries which are not intended to yield multiple rows, you may use the returned N1QLRequest object’s execute() method."""
#bucket1.n1ql_query('UPDATE `class-bucket` set version = "1.0.2" where geometry.type = "MultiPolygon"').execute()
#bucket1.n1ql_query('UPDATE `class-bucket` unset version where geometry.type = "MultiPolygon"').execute()

"""result_set is not subscriptable"""
result_set = bucket1.n1ql_query('select geometry.coordinates from `class-bucket` where properties.ADMIN = "British Indian Ocean Territory"')
# "print(type(result_set))" tells us 'result_set' is a <class 'couchbase.n1ql.N1QLRequest'>
counter = []

"""The return value from n1ql_query() is a N1QLRequest object. 
Iterating over the object will yield the rows returned by the server for the given query (as a dict). 
Each row represents a row received for the query."""

dict = {'key1': 1, 'key2': 2, 'key3': 3}
print(dict.items())

for row in result_set:
    # print(type(row))
    # print(len(row))
    counter.append(row)
print(type(counter[0]['coordinates']))
# print(type(counter[0]))
# print(counter[0].items())
