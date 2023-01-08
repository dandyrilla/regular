from flask import Flask


def create_app():

    # Create an app instance
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'index'

    return app
