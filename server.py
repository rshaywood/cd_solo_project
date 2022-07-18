from flask import Flask
from flask_app import app
from flask_app.controllers import restaurants, users, wishlists
from flask_app.models.restaurant import Restaurant
from flask_app.models.user import User
from flask_app.models.wishlist import Wishlist

if __name__ == "__main__":
    app.run(debug=True)