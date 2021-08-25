from market import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def __init__(self, username, email, password):        
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def purchase(self, item_obj):
        return self.budget >= item_obj.price

    def sell(self, item_obj):
        return item_obj in self.items

    def __repr__(self):
        return f"UserName: {self.username}"

class Item(db.Model):
    user = db.relationship(User)

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __init__(self, name, price, barcode, description, owner):
        self.name = name
        self.price = price
        self.barcode = barcode
        self.description = description
        self.owner = owner

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()