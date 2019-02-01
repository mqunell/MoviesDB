import sys
from PyQt5.QtWidgets import *
from src.gui.tab_add_movie import TabAddMovie
from src.gui.tab_add_movies import TabAddMovies
from src.gui.tab_view_movies import TabViewMovies


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set the window's title
        self.setWindowTitle('Movies DB')

        # Window dimensions and positioning
        width = 520
        height = 465
        left = (1920 - width) / 2
        top = (1080 - height) / 2
        self.setGeometry(left, top, width, height)
        self.setContentsMargins(10, 10, 10, 10)

        # Set up the tabs
        tabs = QTabWidget()

        tab1 = TabAddMovie(self)
        tab2 = TabAddMovies(self)
        tab3 = TabViewMovies(self)

        tabs.addTab(tab1, 'Add Movie (Single)')
        tabs.addTab(tab2, 'Add Movies (Bulk)')
        tabs.addTab(tab3, 'View Movies')

        self.setCentralWidget(tabs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
