from flask import Blueprint, render_template
from screen_sommelier.auth import login_required
from screen_sommelier.movie_fetcher import fetch_and_store_movies, get_db

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def popular():
    fetch_and_store_movies_if_needed()
    popular_movies = get_movies(category='popular')
    top_rated_movies = get_movies(category='top_rated')
    return render_template('popular.html', popular_movies=popular_movies, top_rated_movies=top_rated_movies)

def fetch_and_store_movies_if_needed():
    db = get_db()
    cur = db.execute("SELECT COUNT(*) FROM movies")
    count = cur.fetchone()[0]
    if count == 0:
        fetch_and_store_movies()

def get_movies(category=None):
    db = get_db()
    if category == 'top_rated':
        cur = db.execute("SELECT * FROM movies WHERE category='top_rated'")
    else:
        cur = db.execute("SELECT * FROM movies WHERE category='popular'")
    rows = cur.fetchall()
    return rows
