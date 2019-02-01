from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot

from src.db_connection import DbConnection
from src.omdb_api import get_movie_json
from src.sql import add_series_sql, add_movie_sql


class TabAddMovies(QWidget):

    def __init__(self, main_gui):
        super().__init__()

        self.main_gui = main_gui

        # Multi-line text box
        self.text_edit = QPlainTextEdit(self)
        self.text_edit.move(15, 20)
        self.text_edit.resize(470, 335)

        # Instructions button
        instructions_button = QPushButton('Instructions', self)
        instructions_button.move(15, 365)
        instructions_button.resize(230, 30)
        instructions_button.clicked.connect(self.instructions_button_clicked)

        # Add button
        add_button = QPushButton('Add series/movies', self)
        add_button.move(255, 365)
        add_button.resize(230, 30)
        add_button.clicked.connect(self.add_button_clicked)


    @pyqtSlot()
    def instructions_button_clicked(self):
        instructions = '''
Type one series or movie per line, in the following formats:
SeriesName, NumberMovies
Title, SeriesName, SeriesNumber, Format(s)

Enter \"null\" for SeriesName and SeriesNumber if not applicable.
DVD=1, Bluray=2, 4K Bluray=3, Hard Drive=4, and Streaming=5.

Example:
MCU, 20
Avengers: Infinity War, MCU, 19, 235
Inception, null, null, 14
        '''

        instructions_box = QMessageBox.about(self.main_gui, 'Instructions', instructions)


    @pyqtSlot()
    def add_button_clicked(self):
        input = self.text_edit.toPlainText()

        series_insertions = []
        movie_insertions = []

        for line in input.split('\n'):
            data = line.split(', ')

            if len(data) == 2:
                series_insertions.append(add_series_sql(data[0], data[1]))

            elif len(data) == 4:
                omdb_data = get_movie_json(data[0])
                user_data = {'title': data[0],
                             'series_name': data[1],
                             'series_number': data[2],
                             'formats': data[3]}

                movie_insertions.append(add_movie_sql(user_data, omdb_data))

        if series_insertions != []:
            DbConnection().add_bulk_sql(series_insertions)
        if movie_insertions != []:
            DbConnection().add_bulk_sql(movie_insertions)
