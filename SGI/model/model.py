import logging

from model.graphical_object import GraphicalObject
from view.bounds import Bounds


class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view):
        self.view = view
        self.display_file = []

    def add_object(self, points: list, name: str):
        """Adiciona um objeto gráfico ao display file."""

        self.display_file.append(GraphicalObject(points=points, name=name))
        logging.info(f"Objeto '{name}' adicionado ao display file.")

    def viewport_transform(
        self, points: list, viewport_bounds: Bounds, window_bounds: Bounds
    ) -> list:
        """Transforma as coordenadas do objeto gráfico para o viewport."""

        transformed_points = []

        for point in points:
            x, y = point
            x_viewport = (
                (x - window_bounds.x_min)
                / (window_bounds.x_max - window_bounds.x_min)
                * (viewport_bounds.x_max - viewport_bounds.x_min)
            )

            y_viewport = (
                1 - (y - window_bounds.y_min) / (window_bounds.y_max - window_bounds.y_min)
            ) * (viewport_bounds.y_max - viewport_bounds.y_min)

            transformed_points.append((x_viewport, y_viewport))
