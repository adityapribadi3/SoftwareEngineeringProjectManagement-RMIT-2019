from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

api = Blueprint("api", __name__)

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








