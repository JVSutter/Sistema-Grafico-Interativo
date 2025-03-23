from view.graphical_objects.graphical_object import GraphicalObject
from PyQt6 import QtGui, QtCore


class Point(GraphicalObject):
    """Classe que representa um ponto no viewport."""

    def __init__(self, viewport_points: list):
        self.x, self.y = viewport_points[0]
        print(self.x)
        print(self.y)

    def draw(self, painter: QtGui.QPainter) -> None:
        """Desenha o ponto no viewport."""
        painter.drawEllipse(QtCore.QPointF(self.x, self.y), 3, 3)

    def __str__(self):
        return "Point"
