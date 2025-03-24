from PyQt6 import QtGui, QtWidgets

from utils.bounds import Bounds
from view.graphical_objects.graphical_object import GraphicalObject


class Viewport(QtWidgets.QWidget):
    """Classe responsável por gerenciar o viewport."""

    def __init__(self, parent):
        super().__init__(parent)

        # Define a cor de fundo do viewport
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(100, 0, 0, 100))
        self.setPalette(palette)

        self.viewport_bounds: Bounds = None  # Será definido automaticamente no evento resizeEvent
        self.objects = []

    def resizeEvent(self, event):
        """Sobrescreve o método resizeEvent para atualizar os limites do viewport."""

        super().resizeEvent(event)
        self.viewport_bounds = Bounds(
            x_min=0,
            y_min=0,
            x_max=self.width(),
            y_max=self.height()
        )

    def paintEvent(self, event):
        """Sobrescreve o método paintEvent para desenhar os objetos no viewport."""

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Define a cor e espessura da caneta
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        pen.setWidth(2)
        painter.setPen(pen)

        # Desenha cada objeto
        for obj in self.objects:
            obj.draw(painter)

    def update_viewport(self, objects: list[GraphicalObject]) -> None:
        """Atualiza o viewport."""
        self.objects = objects
        self.update()  # Redesenha o viewport
