import requests
import sqlite3
from flask import current_app, g
from requests.exceptions import ConnectTimeout, HTTPError, Timeout, RequestException

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def fetch_movies(category):
    if category == 'popular':
        url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    elif category == 'top_rated':
        url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYjc4YWI2ZTAzYjNiZDNmNjEwMWQ5MzIwMTZkMTM4NCIsIm5iZiI6MTcyMTk1ODk0Mi4yODIyMzMsInN1YiI6IjY2YTAwZTgzNjE3ZWVjZWViYjI2MTkwZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VGA1Be5og8WjBMLTXpmBZzG9keDk85aa_GMVbSmwB6E"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get('results', [])
    except (ConnectTimeout, HTTPError, Timeout, RequestException) as e:
        print(f"An error occurred: {e}")
        return []

def fetch_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en-US"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYjc4YWI2ZTAzYjNiZDNmNjEwMWQ5MzIwMTZkMTM4NCIsIm5iZiI6MTcyMTk1ODk0Mi4yODIyMzMsInN1YiI6IjY2YTAwZTgzNjE3ZWVjZWViYjI2MTkwZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VGA1Be5og8WjBMLTXpmBZzG9keDk85aa_GMVbSmwB6E"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return {genre['id']: genre['name'] for genre in response.json().get('genres', [])}
    except (ConnectTimeout, HTTPError, Timeout, RequestException) as e:
        print(f"An error occurred: {e}")
        return {}

def insert_movie(conn, movie, genres, category):
    genre_names = ', '.join([genres.get(genre_id, 'Unknown') for genre_id in movie.get('genre_ids', [])])
    sql = ''' INSERT OR IGNORE INTO movies(imdb_id, title, year, rated, released, runtime, genre, director, writer, actors, plot, language, country, awards, metascore, imdb_rating, imdb_votes, box_office, production, website, poster, category)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (
        movie.get('id'),
        movie.get('title'),
        movie.get('release_date', '').split('-')[0],
        '',  # rated is not available in TMDB data
        movie.get('release_date'),
        '',  # runtime is not available in TMDB data
        genre_names,
        '',  # director is not available in TMDB data
        '',  # writer is not available in TMDB data
        '',  # actors is not available in TMDB data
        movie.get('overview'),
        '',  # language is not available in TMDB data
        '',  # country is not available in TMDB data
        '',  # awards is not available in TMDB data
        '',  # metascore is not available in TMDB data
        movie.get('vote_average'),
        movie.get('vote_count'),
        '',  # box_office is not available in TMDB data
        '',  # production is not available in TMDB data
        '',  # website is not available in TMDB data
        f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
        category
    ))
    conn.commit()

def fetch_and_store_movies():
    db = get_db()
    genres = fetch_genres()
    # Fetch and insert popular movies
    popular_movies = fetch_movies('popular')
    for movie in popular_movies:
        insert_movie(db, movie, genres, 'popular')
    # Fetch and insert top-rated movies
    top_rated_movies = fetch_movies('top_rated')
    for movie in top_rated_movies:
        insert_movie(db, movie, genres, 'top_rated')
