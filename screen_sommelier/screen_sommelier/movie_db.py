import os
import requests
import psycopg2
from requests.exceptions import ConnectTimeout, HTTPError, Timeout, RequestException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to get the PostgreSQL database connection directly
def get_db():
    host = os.getenv('PSQLHOST')
    dbname = os.getenv('PSQLDB')
    user = os.getenv('PSQLUSER')
    password = os.getenv('PSQLPWD')
    port = os.getenv('PSQLPORT')
    
    if not all([host, dbname, user, password, port]):
        raise ValueError("One or more PostgreSQL environment variables are not set.")
    
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )
    return conn

# Function to fetch movies based on category
def fetch_movies(category):
    if category == 'popular':
        url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    elif category == 'top_rated':
        url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    
    headers = {
        "accept": "application/json",
        "Authorization": os.getenv('API_KEY')  # Use the API key from the environment variable
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get('results', [])
    except (ConnectTimeout, HTTPError, Timeout, RequestException) as e:
        print(f"An error occurred: {e}")
        return []

# Function to fetch movie genres
def fetch_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": os.getenv('API_KEY')  # Use the API key from the environment variable
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return {genre['id']: genre['name'] for genre in response.json().get('genres', [])}
    except (ConnectTimeout, HTTPError, Timeout, RequestException) as e:
        print(f"An error occurred: {e}")
        return {}

# Function to insert movie details into the database
def insert_movie(conn, movie, genres, category):
    genre_names = ', '.join([genres.get(genre_id, 'Unknown') for genre_id in movie.get('genre_ids', [])])
    sql = ''' INSERT INTO movies(imdb_id, title, year, rated, released, runtime, genre, director, writer, actors, plot, language, country, awards, metascore, imdb_rating, imdb_votes, box_office, production, website, poster, category)
              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
              ON CONFLICT (imdb_id) DO NOTHING'''
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

# Function to fetch and store movies in the database
def fetch_and_store_movies():
    db = get_db()  # Get the database connection
    genres = fetch_genres()

    # Fetch and insert popular movies
    popular_movies = fetch_movies('popular')
    for movie in popular_movies:
        insert_movie(db, movie, genres, 'popular')

    # Fetch and insert top-rated movies
    top_rated_movies = fetch_movies('top_rated')
    for movie in top_rated_movies:
        insert_movie(db, movie, genres, 'top_rated')

    db.close()  # Close the database connection after the operation is done
    print("Movies have been successfully fetched and stored in the database.")

# Execute the function to fetch and store movies
if __name__ == "__main__":
    fetch_and_store_movies()