from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, user_to_check):
        user = User.query.filter_by(name=user_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username")

    def validate_email_address(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email address already registered! Please try a different email address")


    username = StringField(label="Username:", validators=[Length(min=6, max=50), DataRequired()])
    email_address = StringField(label="Email:", validators=[Length(min=6, max=50), Email(), DataRequired()])
    password1 = PasswordField(label="Password:", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo("password1", message="Passwords must match"), DataRequired()])
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Log in")

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase Item!")

class SellItemForm(FlaskForm):
    price = FloatField(label="Price: ", validators=[DataRequired()])
    submit = SubmitField(label="Sell Item!")

class NewItemForm(FlaskForm):
    name = StringField(label="Item name:", validators=[DataRequired()])
    price = FloatField(label="Item price:")
    description = TextAreaField(label="Item Description:", validators=[DataRequired()])
    submit = SubmitField(label="Enlist Item")
