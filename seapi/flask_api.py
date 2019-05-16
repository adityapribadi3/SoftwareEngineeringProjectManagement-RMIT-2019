from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()


class Menu(db.Model):
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

class MenuSchema(ma.Schema):
    
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        fields = ("id", "name", "stock", "price")


menuSchema = MenuSchema(many = True)

# Endpoint to show all food.
@api.route("/showfood", methods = ["GET"])
def getFoods():
    foods = Menu.query.all()
    result = menuSchema.dump(foods)
    return jsonify(result.data)



