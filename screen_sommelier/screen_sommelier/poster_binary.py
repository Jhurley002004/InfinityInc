import os
import requests
import psycopg2
from requests.exceptions import ConnectTimeout, HTTPError, Timeout, RequestException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to get the PostgreSQL database connection
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

# Function to download and convert an image to binary data
def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content  # This returns the image as binary data
    except (ConnectTimeout, HTTPError, Timeout, RequestException) as e:
        print(f"An error occurred while downloading the image: {e}")
        return None

# Function to fetch poster URLs and store images as binary data
def store_posters_as_binary():
    conn = get_db()
    cur = conn.cursor()
    
    # Fetch all movies with a poster URL but no poster_image
    cur.execute("SELECT imdb_id, poster FROM movies WHERE poster IS NOT NULL AND poster_image IS NULL")
    movies = cur.fetchall()
    
    for movie in movies:
        imdb_id, poster_url = movie
        
        # Download the image from the URL
        poster_image = download_image(poster_url)
        
        if poster_image:
            # Update the database with the binary image data
            cur.execute("UPDATE movies SET poster_image = %s WHERE imdb_id = %s", (psycopg2.Binary(poster_image), imdb_id))
            conn.commit()
            print(f"Updated poster image for movie ID {imdb_id}")
        else:
            print(f"Failed to download image for movie ID {imdb_id}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    store_posters_as_binary()