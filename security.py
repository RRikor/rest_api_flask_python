# https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5960168?start=30

from werkzeug.security import safe_str_cmp
from resources.user import UserModel

def authenticate(username, password):
    """
    Function to authenticate our user
    """
    # .get is another way of getting a value from a 
    # dictionary. With added benefit: if no value then None
    user = UserModel.find_by_username(username)
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
    return UserModel.find_by_id(user_id)