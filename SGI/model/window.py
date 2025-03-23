from utils.bounds import Bounds


class Window:
    """Classe que representa a janela de visualização."""

    def __init__(self):
        self.window_bounds = Bounds(x_min=-100, x_max=100, y_min=-100, y_max=100)

    def apply_zoom(self, factor: float) -> None:
        """Aplica um zoom na janela de visualização."""
        self.window_bounds.x_min *= factor
        self.window_bounds.x_max *= factor
        self.window_bounds.y_min *= factor
        self.window_bounds.y_max *= factor

    def apply_pan(self, dx: float, dy: float) -> None:
        """Aplica um pan na janela de visualização."""
        self.window_bounds.x_min += dx
        self.window_bounds.x_max += dx
        self.window_bounds.y_min += dy
        self.window_bounds.y_max += dy
