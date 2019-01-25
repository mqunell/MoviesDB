from PyQt5.QtWidgets import *
from src.omdb_api import get_movie_json
from src.sql import query_series_seriesname_sql, add_movie_sql, add_series_sql, query_movies_sql

import json
import pymysql.cursors


class DbConnection:

    def __init__(self):
        """
        Constructor. Creates the database connection.
        """

        # Parse database information
        with open('data/keys.json') as keys_json_file:
            db_keys = json.load(keys_json_file)['database']

        # Connect to the database
        self.connection = pymysql.connect(host=db_keys['host'],
                                          user=db_keys['user'],
                                          password=db_keys['password'],
                                          db=db_keys['db'],
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)


    def add(self, gui, user_data):
        """
        Controls the flow of checking/adding a series and adding a movie.

        :param gui: The created and initialized GUI
        :param user_data: Dictionary of user-inputted data
        """

        series_name = user_data['series_name']

        # If there is a series name
        if series_name != 'null':

            # If the series isn't found in the database
            if not self.check_series(series_name):

                # If the series is added to the database
                if self.add_series(gui, series_name):
                    self.add_movie(gui, user_data)

            else:
                self.add_movie(gui, user_data)

        else:
            self.add_movie(gui, user_data)


    def check_series(self, series_name):
        """
        Checks if the user-inputted series name already exists in the database.

        :param series_name: The name of the series being checked
        :return: True if the series name is found; False if not
        """

        try:
            with self.connection.cursor() as cursor:

                # Check Series table for the inputted series
                sql = query_series_seriesname_sql(series_name)
                cursor.execute(sql)
                db_series_names = cursor.fetchall()

                if series_name in str(db_series_names):
                    return True

                else:
                    return False

        except:
            raise Exception("Can't access db - check_series")


    def add_series(self, gui, series_name):
        """
        Adds a series to the database after using a QMessageBox to verify.

        :param gui: The created and initialized GUI
        :param series_name: The name of the series being checked
        :return: True if the series was added; False if not
        """

        add_series_box = QMessageBox.question(gui, 'Add Series?', 'That series was not found in the database.\nWould you like to add it?', QMessageBox.Yes, QMessageBox.No)

        if add_series_box == QMessageBox.Yes:
            add_series_num_box = QInputDialog.getInt(gui, 'Series Length?', 'How many movies total are in this series?')
            number_movies = int(add_series_num_box[0])

            try:
                with self.connection.cursor() as cursor:
                    sql = add_series_sql(series_name, number_movies)
                    cursor.execute(sql)

                self.connection.commit()
                return True

            except:
                raise Exception('Can\'t access db - add_series')

        else:
            return False


    def add_movie(self, gui, user_data):
        """
        Adds a movie to the database after using a QMessageBox to verify OMDb data.

        :param gui: The created and initialized GUI
        :param user_data: Dictionary of user-inputted data
        """

        omdb_data = get_movie_json(user_data['title'])
        confirm_box = QMessageBox.question(gui, 'Confirm Movie', f'Does this sound right?\n\"{omdb_data["Plot"]}\"', QMessageBox.Yes, QMessageBox.No)

        if confirm_box == QMessageBox.Yes:

            try:
                with self.connection.cursor() as cursor:

                    sql = add_movie_sql(user_data, omdb_data)
                    cursor.execute(sql)

                self.connection.commit()

            except:
                raise Exception('Can\'t access db - add_movie')


    def add_bulk_sql(self, insertions):
        """
        Adds multiple items to the database.

        :param insertions: List of SQL insert statement strings.
        """

        try:
            with self.connection.cursor() as cursor:
                for insert in insertions:
                    cursor.execute(insert)

            self.connection.commit()

        except:
            raise Exception('Exception - add_bulk_sql')


    def get_movies(self):
        """
        :return: A list of dictionaries where each dictionary is a row in the table.
        """

        try:
            with self.connection.cursor() as cursor:
                sql = query_movies_sql()
                cursor.execute(sql)
                return cursor.fetchall()

        except:
            raise Exception('Exception - get_movies')
