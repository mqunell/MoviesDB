def query_series_sql(series_name):
    """
    Returns the formatted "select SeriesName from Series..." SQL query.

    :param series_name: SeriesName
    :return: Formatted SQL string
    """

    return f'select SeriesName from Series where SeriesName = \"{series_name}\"'


def add_series_sql(series_name, number_movies):
    """
    Returns a formatted "insert into Series..." SQL command.

    :param series_name: SeriesName
    :param number_movies: NumberMovies
    :return: Formatted SQL string
    """

    return f'insert into Series values (\"{series_name}\", {number_movies})'


def add_movie_sql(user_data, omdb_data):
    """
    Parses dictionary/JSON data and returns a formatted "insert into Movie..." SQL command.

    :param user_data: Dictionary of data inputted by user
    :param omdb_data: JSON data from OMDb
    :return: Formatted SQL string
    """

    title = omdb_data['Title']
    year = int(omdb_data['Year'])

    ratings = {'G': 1, 'PG': 2, 'PG-13': 3, 'R': 4}
    rating = ratings[omdb_data['Rated']] if omdb_data['Rated'] in ratings else 5

    minutes = int(omdb_data['Runtime'][:omdb_data['Runtime'].index(' ')])
    runtime = str((minutes // 60)) + ':' + str((minutes % 60))

    genre = omdb_data['Genre']
    director = omdb_data['Director']
    actors = omdb_data['Actors']

    plot = omdb_data['Plot'].replace('"', '\\"')

    poster_link = omdb_data['Poster']

    try:
        metacritic = int(omdb_data['Metascore'])
    except:
        metacritic = -1

    series_name = user_data['series_name']
    if series_name != 'null':
        series_name = f'"{series_name}"'

    series_number = user_data['series_number']
    if series_number != 'null':
        try:
            series_number = int(user_data['series_number'])
        except:
            series_number = -1

    formats = user_data['formats']

    return f'insert into Movie values ("{title}", {year}, {rating}, "{runtime}", "{genre}", "{director}", ' \
           f'"{actors}", "{plot}", "{poster_link}", {metacritic}, {series_name}, {series_number}, "{formats}");'
