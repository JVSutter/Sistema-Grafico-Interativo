import logging
from view.bounds import Bounds


class GraphicalObject:
    """Classe pertinente a objetos gráficos pertencentes ao modelo interno"""

    def __init__(self, points: list, name: str):
        self.points = points
        self.name = name
        
        if len(points) == 1:
            self.type = "Point"
        elif len(points) == 2:
            self.type = "Line"
        else:
            self.type = "Wireframe"

    def transform_points_to_viewport(
        self, viewport_bounds: Bounds, window_bounds: Bounds
    ) -> list:
        """Retorna as coordenadas do objeto gráfico para o viewport."""

        transformed_points = []

        for point in self.points:
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

        logging.info(f"Pontos do objeto {self.name} transformados para viewport: {self.points} -> {transformed_points}")
        return transformed_points

    def __str__(self):
        return f"{self.type} {self.name}: {str(self.points).replace('[', '').replace(']', '')}"
    