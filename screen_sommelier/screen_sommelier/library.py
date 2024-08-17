from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from .auth import login_required
from .db import get_db
import base64
import io

bp = Blueprint('library', __name__, url_prefix = '/library')

@bp.route('/')
def library_home():
    db, curs = get_db()

    curs.execute('SELECT * FROM movies ORDER BY RANDOM() LIMIT 48')
    query = curs.fetchall()
    for movie in query:
        binary_poster = movie['poster_image']
        converted = base64.b64encode(binary_poster).decode('utf-8')
        movie['poster_image'] = converted
        # print(movie)
    return render_template("library/browse.html", first_row = query[0:12], second_row = query[12:24], third_row = query[24:36], fourth_row = query[36:48])

@bp.route('/movie/<id>', methods = ('GET', 'POST'))
def movie(id):
    if request.method == 'POST':
        # The stars for user rating is a form. Each star has a value. 
        # This is a placeholder for adding the user's rating to the db
        pass
    
    db, curs = get_db()

    print(id)
    curs.execute('SELECT * FROM movies WHERE imdb_id = %s', (id,))
    query = curs.fetchone()
    binary = query['poster_image']
    converted = base64.b64encode(binary).decode('utf-8')
    query['poster_image'] = converted

    return render_template('library/movie.html', movie = query)

@bp.route('/settings', methods = ('GET', 'POST'))
def settings():
    if request.method == 'POST':
        setting = request.form['setting']

        if setting == 'subscriptions':
            # Any services checked will have their value in the below list:
            checked_subs = request.form.getlist('subscriptions[]')
            # Awaiting DB configuration to set user's subscriptions
            # Print for now
            print(checked_subs)

        elif setting == 'image':
            new_picture = request.form['new_profile_image']
            # Awaiting DB config to insert user's image
            print('Image received')

        elif setting == 'email':
            new_email = request.form['email']
            # Attempt to update user table here
            print(new_email)

        elif setting == 'username':
            new_username = request.form['email']
            # Attempt to update user table here
            print(new_username)        

    # This can be adjusted to come from the DB if necessary
    services = [
        ('amazon', 'Amazon Video'),
        ('appletv', 'AppleTV'),
        ('max', 'Max'),
        ('disney', 'Disney'),
        ('hulu', 'Hulu'),
        ('netflix', 'Netflix'),
        ('paramount', 'Paramount+'),
        ('peacock', 'Peacock')
    ]

    return render_template('library/settings.html', services = services)