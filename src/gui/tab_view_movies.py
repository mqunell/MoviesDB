from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTreeView

from src.db_connection import DbConnection


class TabViewMovies(QWidget):

    def __init__(self, main_gui):
        super().__init__()

        movies_view = QTreeView()
        movies_view.setRootIsDecorated(False)
        movies_view.setAlternatingRowColors(True)

        layout = QHBoxLayout()
        layout.addWidget(movies_view)
        self.setLayout(layout)

        movies = DbConnection().get_movies()

        table = self.create_table(self)
        movies_view.setModel(table)

        # Translations for database data -> readable data
        self.ratings = {1: 'G', 2: 'PG', 3: 'PG-13', 4: 'R', 5: 'Unrated'}
        self.formats = {1: 'DVD', 2: 'Bluray', 3: '4K Bluray', 4: 'Hard Drive', 5: 'Streaming'}

        for movie in movies:
            self.add_movie(table, movie)

        for i in range(13):
            movies_view.resizeColumnToContents(i)


    def create_table(self, parent):
        """
        Creates and sets up the table.

        :param parent: The parent widget (this class).
        :return: The set up table.
        """

        headers = ['Title', 'Year', 'Rating', 'Runtime', 'Genre', 'Director', 'Actors', 'Plot', 'PosterLink',
                   'Metacritic', 'SeriesName', 'SeriesNumber', 'Format']

        table = QStandardItemModel(0, len(headers), parent)

        for i in range(0, len(headers)):
            table.setHeaderData(i, Qt.Horizontal, headers[i])

        return table


    def add_movie(self, table, movie):
        """
        Creates and fills a row in the table for a movie.

        :param table: The table to be added to.
        :param movie: A dictionary representing a movie from the database.
        """

        current_row = table.rowCount()

        table.insertRow(current_row)

        # Add elements to the row, adjusting them as necessary
        table.setData(table.index(current_row, 0), movie['Title'])
        table.setData(table.index(current_row, 1), movie['Year'])
        table.setData(table.index(current_row, 2), self.ratings[movie['Rating']])
        table.setData(table.index(current_row, 3), str(movie['Runtime'])[:4])
        table.setData(table.index(current_row, 4), movie['Genre'])
        table.setData(table.index(current_row, 5), movie['Director'])
        table.setData(table.index(current_row, 6), movie['Actors'])
        table.setData(table.index(current_row, 7), movie['Plot'])
        table.setData(table.index(current_row, 8), movie['PosterLink'])
        table.setData(table.index(current_row, 9), movie['Metacritic'] if movie['Metacritic'] != -1 else '')
        table.setData(table.index(current_row, 10), movie['SeriesName'])
        table.setData(table.index(current_row, 11), movie['SeriesNumber'])

        formats = ''
        for digit in movie['Format']:
            formats += self.formats[int(digit)] + ', '
        table.setData(table.index(current_row, 12), formats[:-2])
