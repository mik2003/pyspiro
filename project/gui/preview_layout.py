"""Module for the layout of the drawing preview."""

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QVBoxLayout


class PreviewLayout(QVBoxLayout):
    """Class for the layout of the drawing preview."""

    def __init__(self) -> None:
        super().__init__()

        self.drawing_scene = QGraphicsScene()
        self.drawing_scene.addText("Hello!")
        self.drawing_view = QGraphicsView(self.drawing_scene)

        self.addWidget(self.drawing_view)
