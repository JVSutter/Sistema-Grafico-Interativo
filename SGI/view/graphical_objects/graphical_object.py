from abc import ABC, abstractmethod

import numpy as np
from PyQt6 import QtGui


class GraphicalObject(ABC):
    """
    Classe abstrata que representa um objeto gráfico. Cada instância está associada a um
    WorldObject. Mediante qualquer modificação/adição de objetos, o Model passa as representações
    gráficas para a View, que por sua vez, desenha os objetos na tela (invocando o método
    draw() de cada objeto gráfico).
    """

    def __init__(self, viewport_points: np.array):
        self.viewport_points = viewport_points

    @abstractmethod
    def draw(self, painter: QtGui.QPainter) -> None:
        """Desenha o objeto gráfico na tela."""
