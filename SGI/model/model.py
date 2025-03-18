import logging

from model.graphical_object import GraphicalObject
from view.bounds import Bounds


class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view):
        self.view = view
        self.display_file = []

    def add_object(self, points: list, name: str):  # SÓ SUPORTA PONTOS POR ENQUANTO
        """Adiciona um objeto gráfico ao display file."""

        new_obj = GraphicalObject(points=points, name=name, type="point")
        self.display_file.append(new_obj)
        logging.info(f"Objeto '{name}' adicionado ao display file.")

        self.view.draw_object(
            points=new_obj.transform_points_to_viewport(
                self.view.viewport, self.view.window
            )
        )
