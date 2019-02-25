from sqlalchemy.sql import func

from user_server.userServer import db
from itsdangerous import (TimedJSONWebSignatureSerializer
                            as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash



# need to set SECRET_KEY
recipe_list_user_list = db.Table(
                            'recipe_list_user',
                            db.Column(
                                    'user_id',
                                    db.Integer,
                                    db.ForeignKey('users.id'),
                                    primary_key=True
                            ),db.Column(
                                    'recipe_list_id',
                                    db.Integer,
                                    db.ForeignKey('recipelist.id'),
                                    primary_key=True
                            )
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False)

    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    recipe_lists = db.relationship(
        "RecipeList",
        secondary=recipe_list_user_list,
        back_populates='users')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def generate_auth_token(self, expiration=600):
        s = Serializer('hfslb', expires_in=expiration)
        return s.dumps({'id': self.id})

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer('hfslb')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


class RecipeList(db.Model):
    __tablename__ = 'recipelist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    list_name = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    recipes = db.relationship("RecipeTable", back_populates="recipelist")
    users = db.relationship(
        "User",
        secondary=recipe_list_user_list,
        back_populates='recipelist'
    )

class RecipeTable(db.Model):
    # need to restrict recipes so you can't add same recipe twice
    # otherwise there would be a conflict for the primary key
    __tablename__ = 'recipes'
    recipe_list_id = db.Column(
                            db.Integer, db.ForeignKey('recipelist.id'),
                            primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_added = db.Column(db.DateTime, default=func.now(), nullable=False)
"""
tables to add:
    Friends:
        list of people you can share a grocery or recipe list with
        table of three columns. user id, friend id
    grocery list:
        list of groceries. Can add items from recipe database or manually.
        can share list with multiple users
        - table columns
            - item text
            - creator user id
            - date created
            - list name
            - list id

    recipe list:
        list of ids from recipe database
        - table columns:
            - recipe id
            - user id
            - recipe list
            - is shared
            - list name

    grocery list share:
        list of grocery lists with the people they are shared with
        - table columns:
            - grocery list id
            - user id

    recipe list share:
        - table columns:
            - recipe list id
            - user id


"""
