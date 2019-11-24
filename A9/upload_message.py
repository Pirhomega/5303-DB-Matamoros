# will be used to generate random messages
import markovify

# allows me to connect to a cluster
from couchbase.cluster import Cluster

# allows me to access a cluster using a password authetication
from couchbase.cluster import PasswordAuthenticator 

# allows me to issue queries on the cluster
from couchbase.n1ql import N1QLQuery

# allows me to work with json-formatted data
import json

def determine_friend_count():
    

# connect to the cluster
cluster = Cluster('http://127.0.0.1:8091')
authenticator = PasswordAuthenticator('corbinmatamoros', 'MattCorbin')
cluster.authenticate(authenticator)

# open buckets
b_users = cluster.open_bucket('users')
b_messages = cluster.open_bucket('messages')
b_users_connections = cluster.open_bucket('user-connections')
b_users_messages = cluster.open_bucket('user-messages')