class Movie:
    def __init__(self, movie_data):
        self.id = movie_data.get('id')
        self.imdb_id = movie_data.get('imdb_id')
        self.genres = [genre['name'] for genre in movie_data.get('genres', [])]
        self.origin_country = movie_data.get('origin_country')
        self.language = movie_data.get('original_language')
        self.overview = movie_data.get('overview')
        self.poster_path = movie_data.get('poster_path')
        self.release_date = movie_data.get('release_date')
        self.runtime = movie_data.get('runtime')
        self.tagline = movie_data.get('tagline')
        self.title = movie_data.get('title')

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Tagline: {self.tagline}\n"
                f"Release Date: {self.release_date}\n"
                f"Genres: {', '.join(self.genres)}\n"
                f"Overview: {self.overview}\n"
                f"Runtime: {self.runtime} minutes\n"
                f"Original Language: {self.language}"
        )
