from flask import Flask, render_template

from regular import crypto


def create_app():

    # Create an app instance
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(crypto.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
