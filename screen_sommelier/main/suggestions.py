from MovieAPI import MovieAPI
from models import Movie


def make_suggestions(api, liked_movie):

    suggestions = api.get_similar_movies(liked_movie.id)["results"]
    print(f"If you like {liked_movie.title}, you may enjoy:")
    for movie in suggestions:
        print(movie["title"])


if __name__ == '__main__':
    api = MovieAPI()
    movie_data = api.get_movie_by_id("11")
    movie = Movie(movie_data)
    make_suggestions(api, movie)

