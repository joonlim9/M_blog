from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from market import db
from werkzeug.security import generate_password_hash,check_password_hash
from market.models import User, Item
from market.users.forms import RegisterForm, LoginForm


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('items.market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('core.info'))

# @users.route('/market', methods=['GET', 'POST'])
# @login_required
# def market_page():
#     purchase_form = PurchaseItemForm()
#     selling_form = SellItemForm()
#     if request.method == "POST":
#         #Purchase Item Logic
#         purchased_item = request.form.get('purchased_item')
#         p_item_object = Item.query.filter_by(name=purchased_item).first()
#         if p_item_object:
#             if current_user.can_purchase(p_item_object):
#                 p_item_object.buy(current_user)
#                 flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
#             else:
#                 flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
#         #Sell Item Logic
#         sold_item = request.form.get('sold_item')
#         s_item_object = Item.query.filter_by(name=sold_item).first()
#         if s_item_object:
#             if current_user.can_sell(s_item_object):
#                 s_item_object.sell(current_user)
#                 flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
#             else:
#                 flash(f"Something went wrong with selling {s_item_object.name}", category='danger')


#         return redirect(url_for('market_page'))

#     if request.method == "GET":
#         items = Item.query.filter_by(owner=None)
#         owned_items = Item.query.filter_by(owner=current_user.id)
#         return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)