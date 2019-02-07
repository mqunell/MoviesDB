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


    def insert(self, sql_insertion):
        """
        Adds a single item to the database.

        :param sql_insertion: The SQL insert statement string.
        :return: True if successful; False if not.
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_insertion)

            self.connection.commit()
            return True

        except:
            print('insert exception')
            return False


    def insert_bulk(self, sql_insertions):
        """
        Adds multiple items to the database.

        :param sql_insertions: List of SQL insert statement strings.
        :return: True if all successful; False if not.
        """

        try:
            with self.connection.cursor() as cursor:
                for insert in sql_insertions:
                    cursor.execute(insert)

            self.connection.commit()
            return True

        except:
            print('insert_bulk exception')
            return False


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
