import numpy as np

from utils.bounds import Bounds


class Window:
    """Classe que representa a janela de visualização."""

    def __init__(self):
        self.window_bounds = Bounds(x_min=-100, x_max=100, y_min=-100, y_max=100)

    def apply_transformation(self, matrix: np.array) -> None:
        """Aplica uma transformação matricial à janela."""

        window_matrix = np.array(
            [self.window_bounds.x_min, self.window_bounds.y_min],
            [self.window_bounds.x_max, self.window_bounds.y_max],
        )
        window_matrix = np.dot(window_matrix, matrix)

        self.window_bounds = Bounds(*window_matrix[0], *window_matrix[1])
