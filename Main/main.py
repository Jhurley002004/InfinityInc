import requests
from requests.exceptions import ConnectTimeout, HTTPError, Timeout, RequestException
import tkinter as tk
from PIL import Image, ImageTk
import io

def fetch_movie_data():
    omdb_api = "http://www.omdbapi.com/?i=tt3896198&apikey=2219978b"

    try:
        response = requests.get(omdb_api, timeout=10)
        response.raise_for_status()
        return response.json()
    except (ConnectTimeout, HTTPError, Timeout, RequestException) as e:
        print(f"An error occurred: {e}")
        return None

def display_movie_info(movie_data):
    if not movie_data:
        return

    root = tk.Tk()
    root.title("Movie Information")

    # Movie Information
    info_text = (
        f"Title: {movie_data.get('Title', 'Title not found')}\n"
        f"Year: {movie_data.get('Year', 'Year not found')}\n"
        f"Rated: {movie_data.get('Rated', 'Rating not found')}\n"
        f"Released: {movie_data.get('Released', 'Release date not found')}\n"
        f"Runtime: {movie_data.get('Runtime', 'Runtime not found')}\n"
        f"Genre: {movie_data.get('Genre', 'Genre not found')}\n"
        f"Director: {movie_data.get('Director', 'Director not found')}\n"
        f"Writer: {movie_data.get('Writer', 'Writer not found')}\n"
        f"Actors: {movie_data.get('Actors', 'Actors not found')}\n"
        f"Plot: {movie_data.get('Plot', 'Plot not found')}\n"
        f"Language: {movie_data.get('Language', 'Language not found')}\n"
        f"Country: {movie_data.get('Country', 'Country not found')}\n"
        f"Awards: {movie_data.get('Awards', 'Awards not found')}\n"
        f"Metascore: {movie_data.get('Metascore', 'Metascore not found')}\n"
        f"IMDb Rating: {movie_data.get('imdbRating', 'IMDb rating not found')}\n"
        f"IMDb Votes: {movie_data.get('imdbVotes', 'IMDb votes not found')}\n"
        f"Box Office: {movie_data.get('BoxOffice', 'Box office not found')}\n"
        f"Production: {movie_data.get('Production', 'Production not found')}\n"
        f"Website: {movie_data.get('Website', 'Website not found')}\n"
    )

    info_label = tk.Label(root, text=info_text, justify=tk.LEFT)
    info_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Movie Poster
    poster_url = movie_data.get('Poster', None)
    if poster_url:
        response = requests.get(poster_url)
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((300, 450), Image.LANCZOS)  # Resize image to fit the UI
        img_tk = ImageTk.PhotoImage(img)

        poster_label = tk.Label(root, image=img_tk)
        poster_label.image = img_tk
        poster_label.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    movie_data = fetch_movie_data()
    display_movie_info(movie_data)
