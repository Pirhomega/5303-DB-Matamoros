# this script will create a bucket and insert JSON data into it

from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.admin import Admin # the admin class gives me the power to create/delete buckets
from couchbase.n1ql import N1QLQuery

def get_info():
    name = input("Insert name: ")
    age = input("Insert age: ")
    height = input("Insert height in inches: ")
    weight = input("Insert weight in lbs: ")
    email = input("Insert email: ")
    phone = input("Insert phone number: ")
    return name, age, height, weight, email, phone

cluster = Cluster('http://127.0.0.1:8091')
authenticator = PasswordAuthenticator('corbinmatamoros', 'MattCorbin')
cluster.authenticate(authenticator)

adm = Admin('corbinmatamoros','MattCorbin',host='localhost',port=8091)
# adm.bucket_create('class-bucket',bucket_type='couchbase')

#open the 'travel-bucket' within the cluster 'cluster'
bucket1 = cluster.open_bucket('class-bucket')

n, a, h, w, e, p = get_info()

bucket1.upsert(n, {'age':a,'height_in':h,'weight_lbs':w,'contact_info':{'email':e,'phone':p}})
