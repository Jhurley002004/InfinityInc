import os
from flask import Flask, redirect, url_for
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'screen_sommelier.sqlite'),
        DATABASE = {
            'HOST': os.getenv('PSQLHOST'),
            'DB': os.getenv('PSQLDB'),
            'USER': os.getenv('PSQLUSER'),
            'PASSWORD': os.getenv('PSQLPWD'),
            'PORT': os.getenv('PSQLPORT')
        }
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"
    
    @app.route("/")
    def send_to_landing():
        return redirect(url_for('auth.landing_page'))

    # register the database commands
    from . import db

    db.init_app(app)

    from . import auth
    from . import library

    app.register_blueprint(auth.bp)
    app.register_blueprint(library.bp)

    from . import main
    app.register_blueprint(main.bp)

    return app
