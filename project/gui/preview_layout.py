"""Module for the layout of the drawing preview."""

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPolygonF
from PySide6.QtWidgets import (
    QGraphicsPolygonItem,
    QGraphicsScene,
    QGraphicsView,
    QVBoxLayout,
)

from project.core.geometry import n_polygon


class PreviewLayout(QVBoxLayout):
    """Class for the layout of the drawing preview."""

    def __init__(self) -> None:
        super().__init__()

        self.drawing_scene = QGraphicsScene()
        self.drawing_scene.addText("Hello!")
        self.draw_polygon()
        self.drawing_view = QGraphicsView(self.drawing_scene)

        self.addWidget(self.drawing_view)

    def draw_polygon(self) -> None:
        vertices = 100 * n_polygon(13)
        polygon = QPolygonF([QPointF(*p) for p in vertices[0:2, :].T])
        polygon_item = QGraphicsPolygonItem(polygon)
        self.drawing_scene.addItem(polygon_item)
