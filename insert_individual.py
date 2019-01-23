import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from src.add import Add


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = 'Movies DB'
        self.left = 710  # (1920 - 500) / 2
        self.top = 380   # (1080 - 320) / 2
        self.width = 500
        self.height = 445
        self.init_ui()


    def init_ui(self):
        """
        Initializes the GUI and connects widgets to methods.
        """

        # Set the window's title, position, and size
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Common values for placement and different types of widgets
        start_x = 15
        label_w = 200
        label_h = 20
        textbox_w = 470
        textbox_h = 30

        # Title
        title_label = QLabel('Movie title:', self)
        title_label.move(start_x, 30)
        title_label.resize(label_w, label_h)

        self.title_textbox = QLineEdit(self)
        self.title_textbox.move(start_x, 55)
        self.title_textbox.resize(textbox_w, textbox_h)

        # Part of series
        check_series_label = QLabel('Is it part of a series?', self)
        check_series_label.move(start_x, 115)
        check_series_label.resize(label_w, label_h)

        self.check_series_radio_yes = QRadioButton('Yes', self)
        self.check_series_radio_yes.move(start_x, 140)
        self.check_series_radio_yes.resize(50, 20)
        self.check_series_radio_yes.toggled.connect(self.check_series_radio)

        self.check_series_radio_no = QRadioButton('No', self)
        self.check_series_radio_no.move(70, 140)
        self.check_series_radio_no.resize(50, 20)
        self.check_series_radio_no.toggled.connect(self.check_series_radio)

        # Series name
        series_name_label = QLabel('Series name:', self)
        series_name_label.move(start_x, 165)
        series_name_label.resize(label_w, label_h)

        self.series_name_textbox = QLineEdit(self)
        self.series_name_textbox.move(start_x, 190)
        self.series_name_textbox.resize(textbox_w, textbox_h)
        self.series_name_textbox.setEnabled(False)

        # Number in series
        series_num_label = QLabel('Number in series:', self)
        series_num_label.move(start_x, 225)
        series_num_label.resize(label_w, label_h)

        self.series_num_textbox = QLineEdit(self)
        self.series_num_textbox.move(start_x, 250)
        self.series_num_textbox.resize(textbox_w, textbox_h)
        self.series_num_textbox.setEnabled(False)

        # Formats
        formats_label = QLabel('Format(s):', self)
        formats_label.move(start_x, 310)
        formats_label.resize(label_w, label_h)

        self.format_dvd_checkbox = QCheckBox('DVD', self)
        self.format_dvd_checkbox.move(start_x, 335)
        self.format_dvd_checkbox.resize(60, 20)

        self.format_bluray_checkbox = QCheckBox('Bluray', self)
        self.format_bluray_checkbox.move(80, 335)
        self.format_bluray_checkbox.resize(70, 20)

        self.format_4k_checkbox = QCheckBox('4K Bluray', self)
        self.format_4k_checkbox.move(155, 335)
        self.format_4k_checkbox.resize(90, 20)

        self.format_hdd_checkbox = QCheckBox('Hard Drive', self)
        self.format_hdd_checkbox.move(250, 335)
        self.format_hdd_checkbox.resize(100, 20)

        self.format_streaming_checkbox = QCheckBox('Streaming', self)
        self.format_streaming_checkbox.move(355, 335)
        self.format_streaming_checkbox.resize(90, 20)

        # Add button
        add_button = QPushButton('Add movie to database', self)
        add_button.move(start_x, 385)
        add_button.resize(470, 30)
        add_button.clicked.connect(self.add_button_clicked)

        # Show the GUI
        self.show()


    @pyqtSlot(name='QRadioButton')
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


    @pyqtSlot(name='QPushButton')
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

            # Pass this GUI and the user_data to Add
            Add(self, user_data).add()

        else:
            self.statusBar().showMessage('Missing data!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
