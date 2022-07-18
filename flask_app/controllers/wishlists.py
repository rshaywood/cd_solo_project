from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, wishlist, restaurant
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

# CREATE - ROUTES

@app.route('/wishlist/form')
def new_rest_form():
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('wishlist_add.html', this_user=this_user)

@app.route('/wishlist/create', methods=['POST'])
def add_rest():
    if "user_id" not in session:
        return redirect('/')
    if not wishlist.Wishlist.validate_rest_info(request.form):
        return redirect('/wishlist/form')
    data = {
        "name": request.form['name'],
        "street_address": request.form['street_address'],
        "neighborhood": request.form['neighborhood'],
        "user_id" : session['user_id']
    }
    wishlist.Wishlist.add_rest(data)
    return redirect('/wishlist')

# READ - ROUTES

@app.route('/wishlist')
def view_wishlist():
    all_restaurants = wishlist.Wishlist.get_one_users_wishlist({"user_id":session['user_id']})
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('wishlist.html', all_restaurants = all_restaurants, this_user=this_user)

# DELETE - ROUTES

@app.route('/wishlist/delete/<int:id>')
def add_to_faves(data):
    if "user_id" not in session:
        return redirect('/')
    wishlist.Wishlist.remove_and_move_to_faves(data)
    all_restaurants = restaurant.Restaurant.get_one_users_restaurants({"user_id":session['user_id']})
    this_user = user.User.get_user_by_id(session['user_id'])
    return redirect('/dashboard', all_restaurants = all_restaurants, this_user=this_user)
