import logging
from model.graphical_object import GraphicalObject


class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self):
        self.display_file = []

    def add_object(self, coordinates: list, name: str):
        """Adiciona um objeto gráfico ao display file."""
        self.display_file.append(GraphicalObject(points=coordinates, name=name))
        logging.info(f"Objeto '{name}' adicionado ao display file.")
