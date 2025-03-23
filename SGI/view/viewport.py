from PyQt6 import QtWidgets, QtGui
from view.bounds import Bounds
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

        self.viewport_bounds = Bounds(x_min=0, y_min=0, x_max=100, y_max=100)
        self.window_bounds = Bounds(x_min=-50, x_max=50, y_min=-50, y_max=50)

    def update(self, objects: list[GraphicalObject]) -> None:
        """Atualiza o viewport com os objetos gráficos."""

        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.palette().color(QtGui.QPalette.ColorRole.Window))

        for obj in objects:
            obj.draw(self, painter)

        painter.end()
