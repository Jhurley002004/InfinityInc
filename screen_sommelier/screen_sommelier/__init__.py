import os
from flask import Flask, redirect, url_for
from . import db

def create_app():
    app = Flask(__name__)
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'screen_sommelier.sqlite'),
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'screen_sommelier.sqlite'),
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
    # from . import blog
    from . import library

    app.register_blueprint(auth.bp)
    app.register_blueprint(library.bp)

    from . import main
    app.register_blueprint(main.bp)

    return app
