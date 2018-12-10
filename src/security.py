# https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5960168?start=30

from werkzeug.security import safe_str_cmp
from user import User

# This file will contain:
# In memory table of registered users, just pretend this is 
# some sort of database:
# users = [
#     {
#         'id': 1,
#         'username': 'bob'
#         'password': 'asdf'
#     }
# ]
# With using an object User this will become:
users = [
    User(1, 'bob', 'asdf')
]


# A username mapping: So bob is going to be the dictionary 
# of user bob from above.
# username_mapping = { 'bob' : {
#         'id': 1,
#         'username': 'bob',
#         'password', 'asdf'
#     }
# }
# With using an object User this will become a Set Comprehension. But instead
# of assigning values(u for u in users), we assign key value pairs(u.username) 
username_mapping = {u.username: u for u in users}


# In the userid_mapping: the id 1 is going to to be the dictionary
# from user bob again.  
# userid_mapping = { 1: {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# }
# With using an object User this will become:
userid_mapping = {u.id: u for u in users}

# So we created a table of users[]. Then put an index on bob in the 
# username_mapping. And then another index on username 1 in the userid_mapping.
# When this database grows you would be able to do the following:
# username_mapping['bob']
# userid_mapping[1]
# This prevents iterating over our list every time.
# After all of this we transformed the [] to work with the User object.

def authenticate(username, password):
    """
    Function to authenticate our user
    """
    # .get is another way of getting a value from a 
    # dictionary. With added benefit: if no value then None
    user = username_mapping.get(username, None)
    # String comparing with == is dangerous because of String encoding. werkzeug
    # helps with safe_str_cmp to prevent errors. This also works on old python 
    # versions, servers and encodings. 
    if user and safe_str_cmp(user.password, password):
        return user
    
def identity(payload):
    """
    Identity function is unique to flask JWT. It takes
    in a payload with the contents of the JWT token and
    we can extract the user_id from that payload.
    """
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

