from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from src.db_connection import DbConnection
from src.omdb_api import get_movie_json
from src.sql import add_movie_sql, add_series_sql


class TabAddMovie(QWidget):

    def __init__(self, main_gui):
        super().__init__()

        self.main_gui = main_gui

        # Common values for placements and different types of widgets
        start_x = 15
        label_w = 200
        label_h = 20
        textbox_w = 470
        textbox_h = 30

        # Title
        title_label = QLabel('Movie title:', self)
        title_label.move(start_x, 10)
        title_label.resize(label_w, label_h)

        self.title_textbox = QLineEdit(self)
        self.title_textbox.move(start_x, 35)
        self.title_textbox.resize(textbox_w, textbox_h)

        # Part of series
        check_series_label = QLabel('Is it part of a series?', self)
        check_series_label.move(start_x, 95)
        check_series_label.resize(label_w, label_h)

        self.check_series_radio_yes = QRadioButton('Yes', self)
        self.check_series_radio_yes.move(start_x, 120)
        self.check_series_radio_yes.resize(50, 20)
        self.check_series_radio_yes.toggled.connect(self.check_series_radio)

        self.check_series_radio_no = QRadioButton('No', self)
        self.check_series_radio_no.move(70, 120)
        self.check_series_radio_no.resize(50, 20)
        self.check_series_radio_no.toggled.connect(self.check_series_radio)

        # Series name
        series_name_label = QLabel('Series name:', self)
        series_name_label.move(start_x, 145)
        series_name_label.resize(label_w, label_h)

        self.series_name_textbox = QLineEdit(self)
        self.series_name_textbox.move(start_x, 170)
        self.series_name_textbox.resize(textbox_w, textbox_h)
        self.series_name_textbox.setEnabled(False)

        # Number in series
        series_num_label = QLabel('Number in series:', self)
        series_num_label.move(start_x, 205)
        series_num_label.resize(label_w, label_h)

        self.series_num_textbox = QLineEdit(self)
        self.series_num_textbox.move(start_x, 230)
        self.series_num_textbox.resize(textbox_w, textbox_h)
        self.series_num_textbox.setEnabled(False)

        # Formats
        formats_label = QLabel('Format(s):', self)
        formats_label.move(start_x, 290)
        formats_label.resize(label_w, label_h)

        self.format_dvd_checkbox = QCheckBox('DVD', self)
        self.format_dvd_checkbox.move(start_x, 315)
        self.format_dvd_checkbox.resize(60, 20)

        self.format_bluray_checkbox = QCheckBox('Bluray', self)
        self.format_bluray_checkbox.move(80, 315)
        self.format_bluray_checkbox.resize(70, 20)

        self.format_4k_checkbox = QCheckBox('4K Bluray', self)
        self.format_4k_checkbox.move(155, 315)
        self.format_4k_checkbox.resize(90, 20)

        self.format_hdd_checkbox = QCheckBox('Hard Drive', self)
        self.format_hdd_checkbox.move(250, 315)
        self.format_hdd_checkbox.resize(100, 20)

        self.format_streaming_checkbox = QCheckBox('Streaming', self)
        self.format_streaming_checkbox.move(355, 315)
        self.format_streaming_checkbox.resize(90, 20)

        # Add button
        add_button = QPushButton('Add movie to database', self)
        add_button.move(start_x, 365)
        add_button.resize(470, 30)
        add_button.clicked.connect(self.add_button_clicked)


    @pyqtSlot()
    def check_series_radio(self):
        """
        Called when a radio button from "Is it part of a series?" is clicked.
            -Yes: Enables and sets the series name and num text boxes to ''
            -No: Disables and sets the series name and num text boxes to 'null'
        """

        if self.sender().text() == 'Yes':
            self.series_name_textbox.setEnabled(True)
            self.series_num_textbox.setEnabled(True)
            self.series_name_textbox.setText('')
            self.series_num_textbox.setText('')
        else:
            self.series_name_textbox.setEnabled(False)
            self.series_num_textbox.setEnabled(False)
            self.series_name_textbox.setText('null')
            self.series_num_textbox.setText('null')


    @pyqtSlot()
    def add_button_clicked(self):
        """
        Called when the "Add movie to database" button is clicked.
        If the required fields populated, sends the user-inputted data to Add.
        """

        # Swap formats for respective storage values
        formats_output = ''

        if self.format_dvd_checkbox.isChecked():
            formats_output += '1'
        if self.format_bluray_checkbox.isChecked():
            formats_output += '2'
        if self.format_4k_checkbox.isChecked():
            formats_output += '3'
        if self.format_hdd_checkbox.isChecked():
            formats_output += '4'
        if self.format_streaming_checkbox.isChecked():
            formats_output += '5'

        # Ensure that all required fields are populated
        if self.title_textbox.text() != '' and \
                self.series_name_textbox.text() != '' and \
                self.series_num_textbox.text() != '' and \
                formats_output != '':

            # Dictionary of user-inputted data
            user_data = {'title': self.title_textbox.text(),
                         'series_name': self.series_name_textbox.text(),
                         'series_number': self.series_num_textbox.text(),
                         'formats': formats_output}

            self.add_series(user_data)

        else:
            self.main_gui.set_status_bar('Missing data!')


    def add_series(self, user_data):
        """
        Controls the flow of checking/adding a series and adding a movie. Handles the series portion and calls add_movie
        to handle the movie portion.

        :param user_data: Dictionary of user-inputted data
        """

        db_connection = DbConnection()

        series_name = user_data['series_name']

        # If there is a series name
        if series_name != 'null':

            # If the series isn't in the database
            if not db_connection.check_series(series_name):

                # Ask about adding the series; if "Yes" selected
                add_series_box = QMessageBox.question(self.main_gui, 'Add Series?', 'That series was not found in the database.\nWould you like to add it?', QMessageBox.Yes, QMessageBox.No)
                if add_series_box == QMessageBox.Yes:

                    # Ask about series info; if "Ok" selected
                    series_length, add_series_length_box = QInputDialog.getInt(self.main_gui, 'Series Length?', 'How many movies total are in this series?', 1, 1, 30, 1)
                    if add_series_length_box:

                        # If series successfully added
                        if db_connection.insert(add_series_sql(series_name, series_length)):
                            self.main_gui.set_status_bar('Series added!')
                            self.add_movie(user_data)

                        else:
                            self.main_gui.set_status_bar('Add series failed')

                    else:
                        self.main_gui.set_status_bar('Series length cancelled')

                else:
                    self.main_gui.set_status_bar('Add series cancelled')

            else:
                self.add_movie(user_data)

        else:
            self.add_movie(user_data)


    def add_movie(self, user_data):

        # Get and check OMDb data
        omdb_data = get_movie_json(user_data['title'])
        if 'Plot' in omdb_data.keys():

            # Confirm movie
            confirm_movie_box = QMessageBox.question(self.main_gui, 'Confirm Movie', f'Does this sound right?\n\"{omdb_data["Plot"]}\"', QMessageBox.Yes, QMessageBox.No)

            # If "Yes" selected
            if confirm_movie_box == QMessageBox.Yes:
                if DbConnection().insert(add_movie_sql(user_data, omdb_data)):
                    self.main_gui.set_status_bar('Movie added!')

            else:
                self.main_gui.set_status_bar('Add movie cancelled')

        else:
            self.main_gui.set_status_bar('Movie not found on OMDb')
