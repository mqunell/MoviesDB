from src.db_connection import DbConnection
from src.omdb_api import get_movie_json
from src.sql import add_movie_sql, add_series_sql

""""
Adds series and movies from text files
"""

# Read the text files
with open('data/series.txt', 'r') as series_input_file:
    series_input = series_input_file.read().split('\n')

with open('data/movies.txt', 'r') as movies_input_file:
    movies_input = movies_input_file.read().split('\n')


# Insert series data
series_insertions = []

for line in series_input:
    series = line.split(', ')
    series_insertions.append(add_series_sql(series[0], series[1]))


# Insert movies data
movie_insertions = []

for line in movies_input:
    movie = line.split(', ')

    omdb_data = get_movie_json(movie[0])
    user_data = {'title': movie[0],
                 'series_name': movie[1],
                 'series_number': movie[2],
                 'formats': movie[3]}

    movie_insertions.append(add_movie_sql(user_data, omdb_data))


DbConnection().add_bulk_sql(series_insertions)
DbConnection().add_bulk_sql(movie_insertions)
