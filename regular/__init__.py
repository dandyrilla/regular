from flask import Flask

from regular import crypto


def create_app():

    # Create an app instance
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(crypto.bp)

    @app.route('/')
    def index():
        return 'index'

    return app
