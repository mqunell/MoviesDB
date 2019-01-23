import sys
from PyQt5.QtWidgets import *
from gui.tab_add_movie import TabAddMovie


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
        tab2 = QWidget()
        tab3 = QWidget()

        tabs.addTab(tab1, 'Add Movie')
        tabs.addTab(tab2, 'Tab 2')
        tabs.addTab(tab3, 'Tab 3')

        self.setCentralWidget(tabs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
