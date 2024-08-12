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

# Function to fetch movies based on category and page number
def fetch_movies(category, page):
    api_key = os.getenv('API_KEY')  # Use the API key from the environment
    if category == 'popular':
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
    elif category == 'top_rated':
        url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=en-US&page={page}"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"  # Use the access token from the environment variable
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except (ConnectTimeout, HTTPError, Timeout, RequestException) as e:
        print(f"An error occurred: {e}")
        return {}

# Function to fetch movie genres
def fetch_genres():
    api_key = os.getenv('API_KEY')  # Use the API key from the environment variable
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"  # Use the access token from the environment variable
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return {genre['id']: genre['name'] for genre in response.json().get('genres', [])}
    except (ConnectTimeout, HTTPError, Timeout, RequestException) as e:
        print(f"An error occurred: {e}")
        return {}

# Function to fetch movie changes
def fetch_movie_changes(page):
    api_key = os.getenv('API_KEY')  # Use the API key from the environment variable
    url = f"https://api.themoviedb.org/3/movie/changes?api_key={api_key}&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"  # Use the access token from the environment variable
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except (ConnectTimeout, HTTPError, Timeout, RequestException) as e:
        print(f"An error occurred: {e}")
        return {}

# Function to check if a movie already exists in the database
def movie_exists(conn, imdb_id):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM movies WHERE imdb_id = %s", (str(imdb_id),))
    return cur.fetchone() is not None

# Function to insert movie details into the database
def insert_movie(conn, movie, genres, category):
    # Check for required fields
    if not movie.get('title'):
        print(f"Skipping movie with ID {movie.get('id')} due to missing title.")
        return
    
    # Check if the movie already exists
    if movie_exists(conn, str(movie.get('id'))):
        print(f"Movie with ID {movie.get('id')} already exists. Skipping.")
        return
    
    # Validate and format the release date
    release_date = movie.get('release_date')
    if release_date == '':
        release_date = None
    
    sql = ''' 
    INSERT INTO movies(imdb_id, title, year, released, plot, imdb_rating, imdb_votes, poster, category)
    VALUES(%(imdb_id)s, %(title)s, %(year)s, %(released)s, %(plot)s, %(imdb_rating)s, %(imdb_votes)s, %(poster)s, %(category)s) 
    ON CONFLICT (imdb_id) DO NOTHING
    '''
    cur = conn.cursor()
    
    # Prepare the arguments
    args = {
        'imdb_id': str(movie.get('id')),
        'title': movie.get('title'),
        'year': movie.get('release_date', '').split('-')[0] if movie.get('release_date') else None,
        'released': release_date,
        'plot': movie.get('overview'),
        'imdb_rating': movie.get('vote_average'),
        'imdb_votes': movie.get('vote_count'),
        'poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None,
        'category': category
    }
    
    cur.execute(sql, args)
    conn.commit()

    # Insert movie genres into the movie_genre table
    for genre_id in movie.get('genre_ids', []):
        # Check if the genre exists in the genres table
        cur.execute("SELECT 1 FROM genres WHERE genre_id = %s", (genre_id,))
        if not cur.fetchone():
            # If genre does not exist, insert it
            genre_name = genres.get(genre_id, 'Unknown')
            cur.execute("INSERT INTO genres (genre_id, genre_name) VALUES (%s, %s) ON CONFLICT DO NOTHING", (genre_id, genre_name))
            conn.commit()

        # Insert the genre into the movie_genre table
        genre_sql = ''' 
        INSERT INTO movie_genre(movie_id, genre_id) 
        VALUES(%(movie_id)s, %(genre_id)s) 
        ON CONFLICT DO NOTHING
        '''
        genre_args = {
            'movie_id': str(movie.get('id')),
            'genre_id': genre_id
        }
        cur.execute(genre_sql, genre_args)

    conn.commit()

# Function to fetch and store movies in the database
def fetch_and_store_movies():
    db = get_db()  # Get the database connection
    genres = fetch_genres()

    total_movies = 0
    max_movies = 3000

    # Fetch and insert popular movies
    page = 1
    while total_movies < max_movies:
        popular_movies = fetch_movies('popular', page)
        if not popular_movies.get('results'):
            break
        for movie in popular_movies['results']:
            if total_movies >= max_movies:
                break
            insert_movie(db, movie, genres, 'popular')
            total_movies += 1
        page += 1

    # Fetch and insert top-rated movies
    page = 1
    while total_movies < max_movies:
        top_rated_movies = fetch_movies('top_rated', page)
        if not top_rated_movies.get('results'):
            break
        for movie in top_rated_movies['results']:
            if total_movies >= max_movies:
                break
            insert_movie(db, movie, genres, 'top_rated')
            total_movies += 1
        page += 1

    # Fetch and insert movie changes
    page = 1
    while total_movies < max_movies:
        movie_changes = fetch_movie_changes(page)
        if not movie_changes.get('results'):
            break
        for movie in movie_changes['results']:
            if total_movies >= max_movies:
                break
            insert_movie(db, movie, genres, 'changes')
            total_movies += 1
        page += 1

    db.close()  # Close the database connection after the operation is done
    print("Movies have been successfully fetched and stored in the database.")

# Execute the function to fetch and store movies
if __name__ == "__main__":
    fetch_and_store_movies()