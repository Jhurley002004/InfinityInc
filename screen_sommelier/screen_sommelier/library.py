from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from .auth import login_required
from .db import get_db

bp = Blueprint('library', __name__, url_prefix = '/library')

@bp.route('/')
def library_home():
    return render_template("library/browse.html")

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