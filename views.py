from flask import Blueprint, render_template
from models import User, Food

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/food')
def food():
    # Fetch food items from database
    food_items = Food.query.all()
    return render_template('food.html', food_items=food_items)

@views.route('/map')
def map_view():
    return render_template('map.html')
