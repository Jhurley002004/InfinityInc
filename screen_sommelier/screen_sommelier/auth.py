import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Need to add 'email' column to user table then
# get from request.form['email']
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, curs = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                curs.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            # except db.IntegrityError:
            #     error = f"User {username} is already registered."
            except Exception as e:
                error = e
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.landing_page"))

        flash(error)

    return render_template('auth/register.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, curs = get_db()
        curs.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = curs.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.landing_page'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, curs = get_db()
        curs.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = curs.fetchone()


@bp.route('/landing', methods = ('GET', 'POST'))
def landing_page():
    if request.method == 'POST':

        action = request.form["action"]
        print(action)
        if action == "login":
            username = request.form['username']
            password = request.form['password']
            db, curs = get_db()
            error = None
            curs.execute(
                'SELECT * FROM users WHERE username = %s', (username,)
            )
            user = curs.fetchone()
            print(f"The type of user is {type(user)}")
            print(user)
            print(user['id'])

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('library.library_home'))

            flash(error)
            return redirect(url_for('library.library_home'))
        
        elif action == "register":
            # Also need to carry over the email if entered.
            session['email'] = request.form['email']
            return redirect(url_for('auth.register'))
        
    return render_template('/auth/landing_page.html')

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.landing_page"))

        return view(**kwargs)

    return wrapped_view