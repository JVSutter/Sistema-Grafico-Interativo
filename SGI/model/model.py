from model.graphical_object import GraphicalObject
from view.bounds import Bounds


class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view):
        self.view = view
        self.display_file = []

    def add_object(self, points: list, name: str) -> None:
        """Adiciona um objeto gráfico ao display file."""

        graphical_object = GraphicalObject(points=points, name=name)
        self.display_file.append(graphical_object)
