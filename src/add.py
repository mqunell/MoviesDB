from PyQt5.QtWidgets import *
from src.db_connection import get_db_connection
from src.omdb_api import get_movie_json
from src.write_sql import query_series_sql, add_movie_sql, add_series_sql


class Add:

    def __init__(self, gui, user_data):
        """
        :param gui: The created and initialized GUI
        :param user_data: Dictionary of user-inputted data
        """

        self.gui = gui
        self.user_data = user_data
        self.connection = get_db_connection()


    def add(self):
        """
        Controls the flow of checking/adding a series and adding a movie.
        """

        # If there is a series name
        if self.user_data['series_name'] != 'null':

            # If the series isn't found in the database
            if not self.check_series():

                # If the series is added to the database
                if self.add_series():
                    self.add_movie()

            else:
                self.add_movie()

        else:
            self.add_movie()


    def check_series(self):
        """
        Checks if the user-inputted series name already exists in the database.

        :return: True if the series name is found; False if not
        """

        try:
            with self.connection.cursor() as cursor:

                # Check Series table for the inputted series
                sql = query_series_sql(self.user_data['series_name'])
                cursor.execute(sql)
                db_series_names = cursor.fetchall()

                if self.user_data['series_name'] in str(db_series_names):
                    return True

                else:
                    return False

        except:
            raise Exception("Can't access db - check_series")


    def add_series(self):
        """
        Adds a series to the database after using a QMessageBox to verify.
        .
        :return: True if the series was added; False if not
        """

        add_series_box = QMessageBox.question(self.gui, 'Add Series?', 'That series was not found in the database.\nWould you like to add it?', QMessageBox.Yes, QMessageBox.No)

        if add_series_box == QMessageBox.Yes:
            add_series_num_box = QInputDialog.getInt(self.gui, 'Series Length?', 'How many movies total are in this series?')
            number_movies = int(add_series_num_box[0])

            try:
                with self.connection.cursor() as cursor:
                    sql = add_series_sql(self.user_data['series_name'], number_movies)
                    cursor.execute(sql)

                self.connection.commit()
                return True

            except:
                raise Exception('Can\'t access db - add_series')

        else:
            return False


    def add_movie(self):
        """
        Adds a movie to the database after using a QMessageBox to verify OMDb data.
        """

        omdb_data = get_movie_json(self.user_data['title'])
        confirm_box = QMessageBox.question(self.gui, 'Confirm Movie', f'Does this sound right?\n\"{omdb_data["Plot"]}\"', QMessageBox.Yes, QMessageBox.No)

        if confirm_box == QMessageBox.Yes:

            try:
                with self.connection.cursor() as cursor:

                    sql = add_movie_sql(self.user_data, omdb_data)
                    cursor.execute(sql)

                self.connection.commit()

            except:
                raise Exception('Can\'t access db - add_movie')
