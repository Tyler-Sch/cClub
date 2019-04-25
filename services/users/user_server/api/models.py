from sqlalchemy.sql import func

from user_server.userServer import db
from itsdangerous import (TimedJSONWebSignatureSerializer
    as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash


# need to set SECRET_KEY
recipe_list_user_list = db.Table(
    'recipe_list_user_list',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'recipelist_id',
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
        lazy='subquery',
        backref='users')

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
    recipes = db.relationship("Recipes", backref=db.backref("recipelist"))

    def __init__(self, list_creator, list_name):
        self.list_creator = list_creator
        self.list_name = list_name


class Recipes(db.Model):
    # need to restrict recipes so you can't add same recipe twice
    # otherwise there would be a conflict for the primary key

    # also probably need a check to prevent unauthorized user from adding
    # a recipe
    __tablename__ = 'recipes'
    recipe_list_id = db.Column(
                            db.Integer, db.ForeignKey('recipelist.id'),
                            primary_key=True, nullable=False)
    recipe_name = db.Column(db.Text, nullable=False)
    recipe_url = db.Column(db.Text)
    pic_url = db.Column(db.Text)
    recipe_id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_added = db.Column(db.DateTime, default=func.now(), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    has_cooked = db.Column(db.Boolean, default=False, nullable=False)
    date_first_cooked = db.Column(db.DateTime, nullable=True)

    def __init__(
                self, recipe_name, recipe_url, pic_url,
                recipe_list_id, recipe_id, added_by):

        self.recipe_name = recipe_name
        self.recipe_url = recipe_url
        self.pic_url = pic_url
        self.recipe_list_id = recipe_list_id
        self.recipe_id = recipe_id
        self.added_by = added_by

    def get_dict(self):
        data = {
            'name': self.recipe_name,
            'url': self.recipe_url,
            'pic_url': self.pic_url,
            'id': self.recipe_id,
            'added_by': self.added_by
        }
        return data
