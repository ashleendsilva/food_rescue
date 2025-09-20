from flask import Blueprint, request, jsonify, session
from __init__ import db
from models import User, Food

auth = Blueprint('auth', __name__)

# Helper function to get JSON or form data
def get_request_data():
    if request.is_json:
        return request.get_json()
    return request.form.to_dict()

# Signup routes
@auth.route('/signup', methods=['POST'])
def signup_root():
    data = get_request_data()
    role = data.get('role', '').strip().lower()
    
    if role in ['ngo', 'restaurant', 'common']:
        if role == 'ngo':
            return signup_ngo()
        elif role == 'restaurant':
            return signup_restaurant()
        elif role == 'common':
            return signup_common()
    
    return jsonify({
        'status': 'error', 
        'message': 'Please provide a valid role (ngo|restaurant|common)'
    }), 400

@auth.route('/signup/ngo', methods=['POST'])
def signup_ngo():
    data = get_request_data()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    password = data.get('password', '').strip()

    # Validation
    if not all([name, email, phone, password]):
        return jsonify({'status': 'error', 'message': 'All fields are required!'}), 400
    
    if len(password) < 6:
        return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters!'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered!'}), 400

    user = User(name=name, email=email, phone=phone, role='NGO')
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['user_role'] = user.role
        return jsonify({
            'status': 'success', 
            'message': 'NGO registered successfully!',
            'user_id': user.id
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")  # For debugging
        return jsonify({'status': 'error', 'message': 'Registration failed. Please try again.'}), 500

@auth.route('/signup/restaurant', methods=['POST'])
def signup_restaurant():
    data = get_request_data()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    password = data.get('password', '').strip()

    if not all([name, email, phone, password]):
        return jsonify({'status': 'error', 'message': 'All fields are required!'}), 400
    
    if len(password) < 6:
        return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters!'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered!'}), 400

    user = User(name=name, email=email, phone=phone, role='Restaurant')
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['user_role'] = user.role
        return jsonify({
            'status': 'success', 
            'message': 'Restaurant registered successfully!',
            'user_id': user.id
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Registration failed. Please try again.'}), 500

@auth.route('/signup/common', methods=['POST'])
def signup_common():
    data = get_request_data()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    password = data.get('password', '').strip()

    if not all([name, email, phone, password]):
        return jsonify({'status': 'error', 'message': 'All fields are required!'}), 400
    
    if len(password) < 6:
        return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters!'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered!'}), 400

    user = User(name=name, email=email, phone=phone, role='Common')
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['user_role'] = user.role
        return jsonify({
            'status': 'success', 
            'message': 'Registration completed successfully!',
            'user_id': user.id
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Registration failed. Please try again.'}), 500

# Login route
@auth.route('/login', methods=['POST'])
def login():
    data = get_request_data()
    
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', '').strip()

    if not all([email, password, role]):
        return jsonify({'status': 'error', 'message': 'Email, password, and role are required!'}), 400

    # Find user by email and role
    user = User.query.filter_by(email=email, role=role).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['user_role'] = user.role
        return jsonify({
            'status': 'success', 
            'message': f'Welcome back, {user.name}!',
            'user_id': user.id,
            'user_role': user.role
        }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials or role mismatch!'}), 401

# Food management routes
@auth.route('/food/add', methods=['POST'])
def add_food():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please login first!'}), 401
    
    if session.get('user_role') != 'Restaurant':
        return jsonify({'status': 'error', 'message': 'Only restaurants can add food items!'}), 403
    
    data = get_request_data()
    
    title = data.get('title', '').strip()
    quantity = data.get('quantity', '').strip()
    pickup = data.get('pickup', '').strip()
    restaurant = data.get('restaurant', '').strip()
    contact = data.get('contact', '').strip()
    image_url = data.get('image_url', '').strip()
    
    if not all([title, quantity, pickup, restaurant,contact]):
        return jsonify({'status': 'error', 'message': 'Title, quantity, pickup location, restaurant name and contact are required!'}), 400
    
    # Create food item with the current user's ID (NO description field)
    food_item = Food(
        title=title,
        quantity=quantity,
        pickup=pickup,
        restaurant=restaurant,
        contact=contact,
        image_url=image_url if image_url else None,
        user_id=session['user_id']  # Associate food with current user
    )
    
    try:
        db.session.add(food_item)
        db.session.commit()
        return jsonify({
            'status': 'success', 
            'message': 'Food item added successfully!',
            'food_id': food_item.id
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to add food item.'}), 500

@auth.route('/food/available', methods=['GET'])
def get_available_foods():
    """Get all available food items for NGOs"""
    try:
        foods = Food.query.all()
        
        food_list = []
        for food in foods:
            food_list.append({
                'id': food.id,
                'title': food.title,
                'quantity': food.quantity,
                'pickup': food.pickup,
                'restaurant': food.restaurant,
                'contact': food.contact,
                'image_url': food.image_url,
                'restaurant_owner': food.user.name  # Include restaurant owner name
            })
        
        return jsonify({
            'status': 'success',
            'foods': food_list
        }), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to load food items.'}), 500

@auth.route('/food/my-foods', methods=['GET'])
def get_my_foods():
    """Get food items added by the current restaurant"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please login first!'}), 401
    
    if session.get('user_role') != 'Restaurant':
        return jsonify({'status': 'error', 'message': 'Only restaurants can view their food items!'}), 403
    
    try:
        # Now properly filter by user_id to get only the current user's foods
        foods = Food.query.filter_by(user_id=session['user_id']).all()
        
        food_list = []
        for food in foods:
            food_list.append({
                'id': food.id,
                'title': food.title,
                'quantity': food.quantity,
                'pickup': food.pickup,
                'restaurant': food.restaurant,
                'contact': food.contact,
                'image_url': food.image_url
            })
        
        return jsonify({
            'status': 'success',
            'foods': food_list
        }), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to load your food items.'}), 500

@auth.route('/food/delete/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    """Delete a food item (only by the restaurant that created it)"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please login first!'}), 401
    
    if session.get('user_role') != 'Restaurant':
        return jsonify({'status': 'error', 'message': 'Only restaurants can delete food items!'}), 403
    
    try:
        # Find the food item and check if it belongs to the current user
        food = Food.query.filter_by(id=food_id, user_id=session['user_id']).first()
        
        if not food:
            return jsonify({'status': 'error', 'message': 'Food item not found or you do not have permission to delete it!'}), 404
        
        db.session.delete(food)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Food item deleted successfully!'
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to delete food item.'}), 500

@auth.route('/food/update/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    """Update a food item (only by the restaurant that created it)"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please login first!'}), 401
    
    if session.get('user_role') != 'Restaurant':
        return jsonify({'status': 'error', 'message': 'Only restaurants can update food items!'}), 403
    
    try:
        # Find the food item and check if it belongs to the current user
        food = Food.query.filter_by(id=food_id, user_id=session['user_id']).first()
        
        if not food:
            return jsonify({'status': 'error', 'message': 'Food item not found or you do not have permission to update it!'}), 404
        
        data = get_request_data()
        
        # Update fields if provided
        if 'title' in data:
            food.title = data['title'].strip()
        if 'quantity' in data:
            food.quantity = data['quantity'].strip()
        if 'pickup' in data:
            food.pickup = data['pickup'].strip()
        if 'restaurant' in data:
            food.restaurant = data['restaurant'].strip()
        if 'contact' in data:
            food.contact = data['contact'].strip()
        if 'image_url' in data:
            food.image_url = data['image_url'].strip() if data['image_url'].strip() else None
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Food item updated successfully!'
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to update food item.'}), 500

# Logout route
@auth.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out successfully!'}), 200

# Check session status
@auth.route('/status', methods=['GET'])
def check_status():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({
                'status': 'success',
                'logged_in': True,
                'user_id': user.id,
                'user_name': user.name,
                'user_role': user.role
            }), 200
    
    return jsonify({
        'status': 'success',
        'logged_in': False
    }), 200