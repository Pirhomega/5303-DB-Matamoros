from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator

cluster = Cluster('couchbase://localhost:8091')
authenticator = PasswordAuthenticator('corbinmatamoros', 'Matt&Corbin')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('swallows-sample')
cb.upsert('u:king_arthur', {'name': 'Arthur', 'email': 'kingarthur@couchbase.com', 'interests': ['Holy Grail', 'African Swallows']})
# OperationResult<RC=0x0, Key=u'u:king_arthur', CAS=0xb1da029b0000>

cb.get('u:king_arthur').value
# {u'interests': [u'Holy Grail', u'African Swallows'], u'name': u'Arthur', u'email': u'kingarthur@couchbase.com'}

## The CREATE PRIMARY INDEX step is only needed the first time you run this script
cb.n1ql_query('CREATE PRIMARY INDEX ON `swallows-sample`').execute()
from couchbase.n1ql import N1QLQuery
row_iter = cb.n1ql_query(N1QLQuery('SELECT name FROM `swallows-sample` WHERE ' +\
'$1 IN interests', 'African Swallows'))
for row in row_iter: print(row)
# {u'name': u'Arthur'}