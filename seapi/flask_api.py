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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)
    cafeorder = db.relationship('Order', backref='food', lazy=True)


    def __init__(self, name, stock, price, image, description ,id = None):
        self.id = id
        self.name = name
        self.stock = stock
        self.price = price
        self.image = image
        self.description = description

class FoodSchema(ma.Schema):
    
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        fields = ("id", "name", "stock", "price", "image", "description")

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    size = db.Column(db.String(50))
    cafeorder = db.relationship('Order', backref='drink', lazy=True)
    
    def __init__(self, name, price, size, image, description ,id = None):
        self.id = id
        self.name = name
        self.price = price
        self.size = size
        self.image = image
        self.description = description

class DrinkSchema(ma.Schema):
    
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        fields = ("id", "name", "price", "size", "image", "description")

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
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(128), nullable = False)
    cafeorder = db.relationship('Order', backref='user', lazy=True)


    def __init__(self, first_name, last_name, password, email, id = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email

class UserSchema(ma.Schema):
    
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        fields = ("id","first_name", "last_name", "password", "email")

userSchema = UserSchema()

# Endpoint to register user.
@api.route("/register", methods = ["POST"])
def register():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    password = request.json["password"]
    email = request.json["email"]

    newUser = User(first_name, last_name, password, email)

    db.session.add(newUser)
    db.session.commit()

    return userSchema.jsonify(newUser)


# login
@api.route("/login", methods = ["POST"])
def login():
    emails = request.json["email"]
    passwords = request.json["password"]
    emailcheck = User.query.filter_by(email = emails).first()
    passwordcheck = User.query.filter_by(password = passwords).first()

    if not emailcheck or not passwordcheck:
        return jsonify(emails)
    else:
        return jsonify(emails)



#Order
class Order(db.Model):
    __tablename__ = "Cafe_order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'))
   

    def __init__(self, food_id, drink_id, user_id ,id = None):
        self.id = id
        self.food_id = food_id
        self.drink_id = drink_id
        self.user_id = user_id

class OrderSchema(ma.Schema):
    
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        fields = ("food_id", "drink_id", "user_id")

OrderSchema = OrderSchema(many = True)

@api.route("/order", methods = ["POST"])
def order():
    food = request.json["food_id"]
    drink = request.json["drink_id"]
    user = request.json["user_id"]

    newOrder = Order(food, drink, user)

    db.session.add(newOrder)
    db.session.commit()

    return userSchema.jsonify(newOrder)
    


