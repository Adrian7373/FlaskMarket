from email.policy import default

from market import db
from market import bcrypt
from market import login_manager
from flask_login import UserMixin
import locale

try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Float, default=0)
    description = db.Column(db.String(100), nullable=False, unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    is_listed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Item {self.name}"

    def assign_owner(self, current_user, previous_owner):
        self.owner = None
        previous_owner.budget += self.price
        self.owner = current_user.id
        current_user.budget -= self.price
        self.is_listed = False
        db.session.commit()

    def sell(self, new_price):
        self.is_listed = True
        self.price = new_price
        db.session.commit()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    budget = db.Column(db.Float, nullable=False, default=1000)
    owned_items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        return locale.currency(self.budget, grouping=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_buy(self, item_object):
        if item_object.owner == self.id:
            return "owner"
        if self.budget >= item_object.price:
            return "ok"
        else:
            return "balance"


    def can_sell(self, sold_item_object):
        return sold_item_object in self.owned_items