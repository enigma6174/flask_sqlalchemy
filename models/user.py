from db import db


class UserModel(db.Model):

    # Tablename that stores userdata defined by 3 attributes - userid, username, password
    __tablename__ = 'users'

    # Define the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # Initialize user object with user data
    # ID being primary key is auto-generated in the table
    def __init__(self, _username, _password):
        self.username = _username
        self.password = _password

    # Save the user data to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Find the userdata mapped to the client supplied username
    @classmethod
    def find_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # Find the userdata mapped to the client supplied userid
    @classmethod
    def find_userid(cls, uid):
        return cls.query.filter_by(id=uid).first()
