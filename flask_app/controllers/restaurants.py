from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, restaurant
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

# CREATE - ROUTES

@app.route('/restaurant/form')
def new_restaurant_form():
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('add.html', this_user=this_user)

@app.route('/restaurant/create', methods=['POST'])
def add_restaurant():
    if "user_id" not in session:
        return redirect('/')
    if not restaurant.Restaurant.validate_restaurant_info(request.form):
        return redirect('/restaurant/form')
    data = {
        "name": request.form['name'],
        "street_address": request.form['street_address'],
        "neighborhood": request.form['neighborhood'],
        "review": request.form['review'],
        "has_food": request.form['has_food'],
        "user_id" : session['user_id']
    }
    restaurant.Restaurant.add_restaurant(data)
    return redirect('/dashboard')

# READ - ROUTES

@app.route('/dashboard')
def view_dashboard():
    all_restaurants = restaurant.Restaurant.get_one_users_restaurants({"user_id":session['user_id']})
    # all_restaurants = Restaurant.get_one_users_restaurants({"user_id":session['user_id']})
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('dashboard.html', all_restaurants = all_restaurants, this_user=this_user)

@app.route('/restaurant/all_users_restaurants')
def see_every_restaurant():
    every_restaurant = restaurant.Restaurant.get_all_restaurants_with_users()
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('all_restaurants.html', every_restaurant=every_restaurant, this_user=this_user)

@app.route('/restaurant/display/<int:id>')
def display_one_restaurant(id):
    data = {"id":id}
    one_restaurant = restaurant.Restaurant.get_restaurant_by_id(data)
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('view_one.html', one_restaurant = one_restaurant, this_user=this_user)

# UPDATE - ROUTES

@app.route('/restaurant/edit/<int:id>')
def display_edit_restaurant_form(id):
    data = {"id":id}
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('edit.html', one_restaurant = restaurant.Restaurant.get_restaurant_by_id(data), this_user=this_user)

@app.route('/restaurant/<int:id>', methods=['POST'])
def update_restaurant(id):
    if "user_id" not in session:
        return redirect('/')
    if not restaurant.Restaurant.validate_restaurant_info(request.form):
        return redirect(f'/restaurant/edit/{id}')
    data = {
        "name": request.form['name'],
        "street_address": request.form['street_address'],
        "neighborhood": request.form['neighborhood'],
        "review": request.form['review'],
        "has_food": request.form['has_food'],
        "user_id" : session['user_id'],
        'id': request.form['id']
    }
    restaurant.Restaurant.edit_restaurant(data)
    return redirect('/dashboard')

# DELETE - ROUTES

@app.route('/restaurant/delete/<int:id>')
def remove_restaurant(id):
    restaurant.Restaurant.remove_restaurant(id)
    return redirect('/dashboard')