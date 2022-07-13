from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
from flask_app.controllers import restaurants, users
bcrypt = Bcrypt(app) 

class Restaurant:
    db = "foodie_faves"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.street_address = data['street_address']
        self.neighborhood = data['neighborhood']
        self.review = data['review']
        self.has_food = data['has_food']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.diner = None

# CREATE - SQL

    @classmethod
    def add_restaurant(cls, data):
        query = """
        INSERT INTO restaurants (name, street_address, neighborhood, review, has_food, user_id) 
        VALUES (%(name)s, %(street_address)s, %(neighborhood)s, %(review)s, %(has_food)s, %(user_id)s)
        ;"""
        restaurant_id = connectToMySQL(cls.db).query_db(query,data)
        return restaurant_id

# READ - SQL

    @classmethod
    def get_one_users_restaurants(cls, data):
        query = """
        SELECT *
        FROM restaurants
        WHERE user_id = %(user_id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        one_users_restaurants = []
        if not result:
            return result
        for row in result:
            one_restaurant = cls(row)            
            one_users_restaurants.append(one_restaurant)
        return one_users_restaurants    

    @classmethod
    def get_restaurant_by_id(cls, data):
        query = """
        SELECT * FROM restaurants
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

# UPDATE - SQL

    @classmethod
    def edit_restaurant(cls, data):
        query = """
        UPDATE restaurants SET name = %(name)s, street_address = %(street_address)s, neighborhood = %(neighborhood)s, review = %(review)s, has_food = %(has_food)s, created_at = NOW(), updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

# DELETE - SQL

    @classmethod
    def remove_restaurant(cls, id):
        data = { 'id': id }
        query = "DELETE FROM restaurants WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

# VALIDATE - SQL

    @staticmethod
    def validate_restaurant_info(restaurant):
        is_valid = True
        query = "SELECT * FROM restaurants WHERE id = %(id)s;"
        results = connectToMySQL(Restaurant.db).query_db(query, restaurant)
        print(results)
        if not restaurant['name']:
            flash("Name of restaurant must be at least 3 characters.","create_restaurant")
            is_valid= False
        if len(restaurant['street_address']) < 3:
            flash("Please enter valid street address.","create_restaurant")
            is_valid= False
        if len(restaurant['neighborhood']) < 3:
            flash("Neighborhood must be at least 3 characters.","create_restaurant")
            is_valid= False
        if len(restaurant['review']) < 3:
            flash("Review of restaurant must be at least 3 characters.","create_restaurant")
            is_valid= False         
        return is_valid