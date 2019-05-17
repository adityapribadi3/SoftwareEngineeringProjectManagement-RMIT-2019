from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask_cors import CORS

api = Blueprint("api", __name__)
CORS(api)

db = SQLAlchemy()
ma = Marshmallow()

#FOOD
class Food(db.Model):
    __tablename__ = "food"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text)
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, name, stock, price, id = None):
        self.id = id
        self.name = name
        self.stock = stock
        self.price = price

class FoodSchema(ma.Schema):
    
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        fields = ("id", "name", "stock", "price")

foodSchema = FoodSchema(many = True)

# Endpoint to show all food.
@api.route("/showfood", methods = ["GET"])
def getFoods():
    foods = Food.query.all()
    result = foodSchema.dump(foods)
    return jsonify(result.data)

#DRINK
class Drink(db.Model):
    __tablename__ = "drink"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text)
    price = db.Column(db.Integer)
    size = db.Column(db.Text)

    def __init__(self, name, price, size, id = None):
        self.id = id
        self.name = name
        self.price = price
        self.size = size

class DrinkSchema(ma.Schema):
    
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        fields = ("id", "name", "price", "size")

drinkSchema = DrinkSchema(many = True)

# Endpoint to show all drink.
@api.route("/showdrink", methods = ["GET"])
def getDrinks():
    drinks = Drink.query.all()
    result = drinkSchema.dump(drinks)
    return jsonify(result.data)

#REGISTER
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)

    def __init__(self, name, password, email, id = None):
        self.id = id
        self.name = name
        self.password = password
        self.email = email

class UserSchema(ma.Schema):
    
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        fields = ("id","name", "password", "email")

userSchema = UserSchema()

# Endpoint to register user.
@api.route("/register", methods = ["POST"])
def register():
    name = request.json["name"]
    password = request.json["password"]
    email = request.json["email"]

    newUser = User(name, password, email)

    db.session.add(newUser)
    db.session.commit()

    return userSchema.jsonify(newUser)






