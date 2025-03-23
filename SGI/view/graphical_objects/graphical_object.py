from abc import ABC, abstractmethod
from PyQt6 import QtGui


class GraphicalObject(ABC):
    """Classe abstrata que representa um objeto gráfico."""

    def __init__(self, viewport_points: list):
        self.viewport_points = viewport_points

    @abstractmethod
    def draw(self, painter: QtGui.QPainter) -> None:
        """Desenha o objeto gráfico na tela."""
