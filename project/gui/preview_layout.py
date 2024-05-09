"""Module for the layout of the drawing preview."""

import pyqtgraph as pg  # type: ignore
from PySide6.QtWidgets import QVBoxLayout


class PreviewLayout(QVBoxLayout):
    """Class for the layout of the drawing preview."""

    def __init__(self) -> None:
        super().__init__()

        self.plot_widget = pg.PlotWidget(background="white")
        self.plot_widget.setXRange(-1, 1)
        self.plot_widget.setYRange(-1, 1)

        self.graph = self.plot_widget.plot(pen="black")

        self.plot_widget.setMaximumWidth(500)
        self.addWidget(self.plot_widget)
