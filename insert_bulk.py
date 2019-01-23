from src.db_connection import get_db_connection
from src.omdb_api import get_movie_json
from src.write_sql import add_movie_sql, add_series_sql

""""
Adds series and movies from text files
"""

# Read the text files
with open('data/series.txt', 'r') as series_input_file:
    series_input = series_input_file.read().split('\n')

with open('data/movies.txt', 'r') as movies_input_file:
    movies_input = movies_input_file.read().split('\n')


connection = get_db_connection()

# Add data to database
try:
    with connection.cursor() as cursor:

        # Insert series data
        for line in series_input:
            series = line.split(', ')
            sql = add_series_sql(series[0], series[1])
            cursor.execute(sql)

        # Insert movies data
        for line in movies_input:
            movie = line.split(', ')

            omdb_data = get_movie_json(movie[0])
            user_data = {'title': movie[0],
                         'series_name': movie[1],
                         'series_number': movie[2],
                         'formats': movie[3]}

            sql = add_movie_sql(user_data, omdb_data)
            cursor.execute(sql)

    # Commit the changes
    connection.commit()

finally:
    connection.close()
