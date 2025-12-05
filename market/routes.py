from flask import render_template, redirect, url_for, flash, request
from unicodedata import category

from market import app
from market.models import User, Item
from market import forms
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = forms.PurchaseItemForm()
    selling_form = forms.SellItemForm()
    new_item_form = forms.NewItemForm()
    if request.method == "POST":
    # Purchase Logic
        item_id= request.form.get('purchased_item')
        item_object = Item.query.get(item_id)
        if item_object:
            previous_owner_id = item_object.owner
            previous_owner = User.query.get(previous_owner_id)
            if current_user.can_buy(item_object) == "ok":
                item_object.assign_owner(current_user, previous_owner)
                flash(f"Congratulations! You have bought {item_object.name} for {item_object.price}", category="success")
            elif current_user.can_buy(item_object) == "owner":
                flash("You cannot purchase your listings", category="info")
            else:
                flash("Insufficient balance! Please increase balance", category="danger")


    # Sell Logic
        sold_item_price = selling_form.price.data
        sold_item_id = request.form.get('sold_item')
        sold_item_object = Item.query.get(sold_item_id)
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(sold_item_price)
                flash(f"Congratulations! You have listed {sold_item_object.name} for {sold_item_object.price}",
                      category="success")
            else:
                flash(f"Something went wrong, cannot sell {sold_item_object.name}", category="danger")

        if new_item_form.validate_on_submit():
            current_user_id = current_user.id
            item_to_enlist = Item(name=new_item_form.name.data,
                                  price=new_item_form.price.data,
                                  description=new_item_form.description.data,
                                  owner=current_user_id)
            db.session.add(item_to_enlist)
            db.session.commit()
            flash(f"Congratulations! You have enlisted {new_item_form.name.data}")

        return redirect(url_for('market_page'))


    if request.method == "GET":
        items = Item.query.filter_by(is_listed=True)
        owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('market.html', items=items,owned_items=owned_items,
                           purchase_form=purchase_form,
                           selling_form=selling_form,
                           new_item_form=new_item_form,
                           current_user=current_user)

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.username.data,
                              email=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account Successfully Created. You are logged in as {user_to_create.name}")
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg)
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET','POST'])
def login_page():
    form = forms.LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(name=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash("Login Successful!", category='success')
            return redirect(url_for('market_page'))
        else:
            flash("Wrong username or password!", category="danger")
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("logged out successfully!", category="success")
    return redirect(url_for('home_page'))