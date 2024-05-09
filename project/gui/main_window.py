""" Module for the initialization of the main window. """

from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QWidget

from project.gui.inputs_layout import InputsLayout
from project.gui.preview_layout import PreviewLayout


class MainWindow(QMainWindow):
    """Class containing the main ui window."""

    def __init__(self) -> None:
        super().__init__()

        # Setup of the Main Layout
        self.main_layout = QHBoxLayout()

        # Central widget of the program
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.main_layout)

        # Setup of the Main Window
        self.setCentralWidget(self.central_widget)
        self.resize(800, 500)

        # Setup of the layout
        self.preview_layout = PreviewLayout()
        self.inputs_layout = InputsLayout(preview=self.preview_layout)

        self.main_layout.addLayout(self.preview_layout)
        self.main_layout.addLayout(self.inputs_layout)
