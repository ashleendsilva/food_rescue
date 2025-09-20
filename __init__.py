from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# --- Database ---
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    # Import models
    from models import User, Food

    # Import blueprints
    from views import views
    from auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Create tables if they don't exist ---
    with app.app_context():
        db.create_all()
        print("✅ Database tables created or already exist.")

    return app
