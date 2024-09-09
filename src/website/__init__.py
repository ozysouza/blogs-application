import os

from flask import render_template, abort
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from src.helpers.forms import LoginForm
from src.website.auth import login


def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    # Directory to save uploaded images from CKEditor
    app.config['UPLOAD_FOLDER'] = 'website/static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # Initialize Bootstrap
    Bootstrap5(app)

    # Register Blueprints
    from .views import views
    app.register_blueprint(views)

    from .auth import auth
    app.register_blueprint(auth)

    from .upload import upload
    app.register_blueprint(upload)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Set the login route

    @app.errorhandler(403)
    def forbidden(err):
        login_form = LoginForm()
        return render_template('error.html', login_form=login_form), 403

    @login_manager.unauthorized_handler
    def unauthorized():
        return abort(403)

    # Define user_loader callback inside create_app
    from src.helpers.models import User
    from .auth import user_manager
    @login_manager.user_loader
    def load_user(user_id):
        user_data = user_manager.get_by_id(user_id)
        if user_data:
            return user_data
        return None

    return app
