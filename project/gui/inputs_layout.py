"""Module for the layout of inputs."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider, QVBoxLayout


class InputsLayout(QVBoxLayout):
    """Class for the layout of inputs."""

    def __init__(self) -> None:
        super().__init__()
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 1)
        self.addWidget(slider)
