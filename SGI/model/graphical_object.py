import logging
from view.bounds import Bounds


class GraphicalObject:
    """Classe pertinente a objetos gráficos pertencentes ao modelo interno"""

    def __init__(self, points: list, name: str):
        self._points = points
        self._name = name
        self._type = self._determine_type()
        
    def _determine_type(self):
        """Determina o tipo do objeto com base no número de pontos."""
        if len(self._points) == 1:
            return "Point"
        elif len(self._points) == 2:
            return "Line"
        else:
            return "Wireframe"
            
    @property
    def points(self):
        """Getter para os pontos do objeto."""
        return self._points
        
    @property
    def name(self):
        """Getter para o nome do objeto."""
        return self._name
        
    @property
    def type(self):
        """Getter para o tipo do objeto."""
        return self._type

    def transform_points_to_viewport(
        self, viewport_bounds: Bounds, window_bounds: Bounds
    ) -> list:
        """Retorna as coordenadas do objeto gráfico para o viewport."""
        transformed_points = []

        for point in self._points:
            x, y = point

            x_viewport = self._transform_x_to_viewport(x, viewport_bounds, window_bounds)
            y_viewport = self._transform_y_to_viewport(y, viewport_bounds, window_bounds)

            transformed_points.append((x_viewport, y_viewport))

        logging.info(f"Pontos do objeto {self._name} transformados para viewport: {self._points} -> {transformed_points}")
        return transformed_points
        
    def _transform_x_to_viewport(self, x, viewport_bounds, window_bounds):
        """Transforma a coordenada X do mundo para o viewport."""
        return (
            (x - window_bounds.x_min)
            / (window_bounds.x_max - window_bounds.x_min)
            * (viewport_bounds.x_max - viewport_bounds.x_min)
        )
        
    def _transform_y_to_viewport(self, y, viewport_bounds, window_bounds):
        """Transforma a coordenada Y do mundo para o viewport."""
        return (
            1 - (y - window_bounds.y_min) / (window_bounds.y_max - window_bounds.y_min)
        ) * (viewport_bounds.y_max - viewport_bounds.y_min)

    def __str__(self):
        return f"{self._type} {self._name}: {str(self._points).replace('[', '').replace(']', '')}"
