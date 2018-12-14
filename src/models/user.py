from db import db

# Extending db.Model to tell SQLAlchemy that this class
# will save things to a db..
class UserModel(db.Model):

    # SQLAlchemy definitions for the table 'users'
    # Properties not defined here will not be saved into the db
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        # id is a python keyword and we don't want to use that as a variable id. 
        # thus we use _id. But self.id works fine. 
        # self.id = _id
        # By using sqlalchemy it is not necessary to supply an ID here
        self.username = username
        self.password = password

    # Because of calling the class User, we can use the @classmethod tag. This is 
    # not necessary, but slightly nicer.
    @classmethod
    def find_by_username(cls, username):
        # filter_by: first username = db, second username is function parameter
        # first() returns the first row
        return cls.query.filter_by(username=username).first()

    # Copy paste from find_by_username, adapted to kd
    @classmethod
    def find_by_id(cls, _id):
        # filter_by: first id= db, second _id is function parameter
        # first() returns the first row
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

