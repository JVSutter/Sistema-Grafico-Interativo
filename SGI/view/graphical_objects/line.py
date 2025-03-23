from view.graphical_objects.graphical_object import GraphicalObject
from PyQt6 import QtGui, QtCore


class Line(GraphicalObject):
    """Classe que representa o segmento de reta no viewport."""

    def __init__(self, viewport_points: list):
        self.point_a, self.point_b = viewport_points

    def draw(self, painter: QtGui.QPainter) -> None:
        """Desenha o segmento de reta no viewport."""
        x1, y1 = self.point_a
        x2, y2 = self.point_b
        painter.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))
