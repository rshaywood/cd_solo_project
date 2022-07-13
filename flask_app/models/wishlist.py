from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
from flask_app.controllers import wishlists, users
bcrypt = Bcrypt(app) 

class Wishlist:
    db = "foodie_faves"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.street_address = data['street_address']
        self.neighborhood = data['neighborhood']
        # self.review = data['review']
        # self.has_food = data['has_food']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.diner = None

# CREATE - SQL

    @classmethod
    def add_restaurant(cls, data):
        query = """
        INSERT INTO wishlist (name, street_address, neighborhood, user_id) 
        VALUES (%(name)s, %(street_address)s, %(neighborhood)s, %(user_id)s)
        ;"""
        restaurant_id = connectToMySQL(cls.db).query_db(query,data)
        return restaurant_id

# READ - SQL

    @classmethod
    def get_one_users_wishlist(cls, data):
        query = """
        SELECT *
        FROM wishlist
        WHERE user_id = %(user_id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        one_users_wishlist = []
        if not result:
            return result
        for row in result:
            one_restaurant = cls(row)            
            one_users_wishlist.append(one_restaurant)
        return one_users_wishlist  

# UPDATE - SQL
    
    @classmethod
    def remove_and_move_to_faves(cls, data):
        query = """
        CREATE TRIGGER before_restaurant_delete
        BEFORE DELETE
        ON wishlist FOR EACH ROW
        BEGIN
        INSERT INTO restaurants (name, street_address, neighborhood, user_id)
        VALUES(%(name)s, %(street_address)s, %(neighborhood)s, %(user_id)s)
        ;"""
        restaurant_id = connectToMySQL(cls.db).query_db(query,data)
        return restaurant_id

# DELETE - SQL

    # @classmethod
    # def remove_restaurant(cls, id):
    #     data = { 'id': id }
    #     query = "DELETE FROM wishlist WHERE id = %(id)s;"
    #     return connectToMySQL(cls.db).query_db(query, data)

# VALIDATE - SQL

    @staticmethod
    def validate_restaurant_info(restaurant):
        is_valid = True
        query = "SELECT * FROM wishlist WHERE id = %(id)s;"
        results = connectToMySQL(Wishlist.db).query_db(query, restaurant)
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
        return is_valid