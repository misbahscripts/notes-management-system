from flask import Flask
from flask_login import LoginManager
from .models import db, User

def create_app():
    app = Flask(__name__)

    # 🛡️ Config
    app.config['SECRET_KEY'] = 'fuckinghelooow'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 💾 DB Init
    db.init_app(app)

    # 🔐 Login Manager Init
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # redirect if not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # 🔁 Load user from DB

    # 📦 Register Blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    # ✅ Create DB tables
    with app.app_context():
        db.create_all()
        print("✅ Database created!")

    return app
