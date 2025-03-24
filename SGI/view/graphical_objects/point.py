import numpy as np
from PyQt6 import QtCore, QtGui

from view.graphical_objects.graphical_object import GraphicalObject


class Point(GraphicalObject):
    """Classe que representa um ponto no viewport."""

    def draw(self, painter: QtGui.QPainter) -> None:
        """Desenha o ponto no viewport."""
        x, y = self.viewport_points[0]
        painter.drawEllipse(QtCore.QPointF(x, y), 3, 3)
