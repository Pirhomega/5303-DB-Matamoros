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

# allows me to create timestamps and track execution time of this program
from datetime import datetime
import time

# allows to generate random numbers
import random

# allows me to find the computer's ip address
import socket

def train_model():
    # Get raw text as string.
    with open("/Users/student/Desktop/1.txt", errors ="ignore") as a:
        text_a = a.read()
    with open("/Users/student/Desktop/2.txt", errors="ignore") as b:
        text_b = b.read()
    with open("/Users/student/Desktop/3.txt", errors ="ignore") as c:
        text_c = c.read()
    with open("/Users/student/Desktop/4.txt", errors="ignore") as d:
        text_d = d.read()

    # Build the models
    model_a = markovify.Text(text_a)
    model_b = markovify.Text(text_b)
    model_c = markovify.Text(text_c)
    model_d = markovify.Text(text_d)

    # Combine the models. The numbers indicate how much weight to give a particular model
    model_combo = markovify.combine([ model_a, model_b, model_c, model_d ], [ 1, 1, 1, 1 ])

    return model_combo

# generate a message and upload to database
def generate_messages(row, b_messages, b_users_messages, model, user, message_num):
    for count in range(0,message_num):
        # generate the message from trained model
        message = model.make_short_sentence(100)

        # generate a random timestamp for message
        now = int(datetime.timestamp(datetime.now()))
        timestmp = datetime.fromtimestamp(random.randint(0,now))

        # who will receive the message
        index = random.randint(0,len(row)-1)
        recipient = row[index]

        # ip address of this computer
        ipaddress = socket.gethostbyname(socket.gethostname())

        # upload database with message and connection info between sender and receiver
        b_messages.upsert(ipaddress+'::'+str(user)+'_'+str(count),{'message':message, 'create_time':str(timestmp)})
        b_users_messages.upsert(ipaddress+'::'+str(user)+'_'+str(count),{'from':user, 'to':recipient})

start = time.perf_counter()

# connect to the cluster
cluster = Cluster('http://10.0.88.237:8091')
authenticator = PasswordAuthenticator('CorbinMatamoros', 'MattCorbin')
cluster.authenticate(authenticator)

# open buckets
b_users = cluster.open_bucket('users')
b_messages = cluster.open_bucket('messages')
b_users_connections = cluster.open_bucket('user-connections')
b_users_messages = cluster.open_bucket('user-messages')

# train and return a trained model for generating random messages
model = train_model()

for user in range(0,10000):
    query_string = "select friends from `user-connections` where user_id = $1"
    result = b_users.n1ql_query(N1QLQuery(query_string, user))
    for row in result:
        message_num = random.randint(0,93)
        generate_messages(row["friends"], b_messages, b_users_messages, model, user, message_num)

execution_time = time.perf_counter() - start
print(execution_time)
