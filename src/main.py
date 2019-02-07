import sys
from PyQt5.QtWidgets import *
from src.gui.tab_add_movie import TabAddMovie
from src.gui.tab_add_movies import TabAddMovies
from src.gui.tab_view_movies import TabViewMovies


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set the window's title
        self.setWindowTitle('MoviesDB')

        # Window dimensions and positioning
        width = 1200
        height = 600
        left = (1920 - width) / 2
        top = (1080 - height) / 2
        self.setGeometry(left, top, width, height)
        self.setContentsMargins(10, 10, 10, 10)

        # Set up the tabs
        tabs = QTabWidget()
        tabs.currentChanged.connect(self.tab_changed)

        tab1 = TabViewMovies(self)
        tab2 = TabAddMovie(self)
        tab3 = TabAddMovies(self)

        tabs.addTab(tab1, 'View Movies')
        tabs.addTab(tab2, 'Add Movie (Single)')
        tabs.addTab(tab3, 'Add Movies (Bulk)')

        self.setCentralWidget(tabs)


    def tab_changed(self, tab_index):
        """
        Called automatically when the user changes tabs.
        Note: Since this is called automatically when the GUI is created, it pseudo-creates padding for the status bar.

        :param tab_index: The index of the newly-selected tab.
        """

        self.set_status_bar('')

        if tab_index in (1, 2):
            self.setGeometry(self.geometry().left(), self.geometry().top(), 520, 485)

        else:
            self.setGeometry(self.geometry().left(), self.geometry().top(), 1200, 600)


    def set_status_bar(self, message):
        """
        Helper method for setting the status bar message.

        :param message: The message to set.
        """

        self.statusBar().showMessage(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
