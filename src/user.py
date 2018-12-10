# https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5960168?start=30
# User object file

class User:
    def __init__(self, _id, username, password):
        # id is a python keyword and we don't want to use that as a variable id. 
        # thus we use _id. But self.id works fine. 
        self.id = _id
        self.username = username
        self.password = password