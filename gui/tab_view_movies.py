from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QStandardItemModel
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

        # todo: fix db_connection constructor/method params so passing Nones isn't necessary
        movies = DbConnection(None, None).get_movies()

        model = self.create_model(self)
        movies_view.setModel(model)

        for movie in movies:
            self.add_movie(model, movie)


    def create_model(self, parent):
        headers = ['Title', 'Year', 'Rating', 'Runtime', 'Genre', 'Director', 'Actors', 'Plot', 'PosterLink',
                   'Metacritic', 'SeriesName', 'SeriesNumber', 'Format']

        model = QStandardItemModel(0, len(headers), parent)

        for i in range(0, len(headers)):
            model.setHeaderData(i, Qt.Horizontal, headers[i])

        return model


    def add_movie(self, model, movie):
        dict_keys = list(movie)

        current_row = model.rowCount()

        model.insertRow(current_row)

        for i in range(0, len(movie)):
            model.setData(model.index(current_row, i), movie[dict_keys[i]])
