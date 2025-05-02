import numpy as np

from model.transformation_generator import TransformationGenerator
from utils.bounds import Bounds


class Window:
    """Classe que representa a janela de visualização."""

    def __init__(self, viewport_bounds: Bounds):
        """
        Como o tamanho do viewport é determinado em tempo de execução,
        adequamos o tamanho da janela de visualização para manter a proporção. De
        outra forma, a imagem seria distorcida.
        """

        viewport_width = viewport_bounds.x_max - viewport_bounds.x_min
        viewport_height = viewport_bounds.y_max - viewport_bounds.y_min
        aspect_ratio = viewport_width / viewport_height

        self.height = 20  # Valor default
        self.width = self.height * aspect_ratio

        # O centro da Window foi escolhido como o VRP (View Reference Point) por conveniência
        self.window_center = np.array([0.0, 0.0, 0.0, 1.0])

        # Vetores da window: um apontando pra cima, um apontando pra direita e um apontando pra frente
        self.vup = np.array([0.0, 1.0, 0.0, 1.0])
        self.vright = np.array([1.0, 0.0, 0.0, 1.0])
        self.view_plane_normal = np.array(
            [0.0, 0.0, 1.0, 1.0]
        )  # Window começa sobre o plano xy, olhando em direção a z positivo

        self.window_bounds = Bounds(
            x_min=-self.width,
            x_max=self.width,
            y_min=-self.height,
            y_max=self.height,
        )

        self.zoom_level = 1.0
        self.angle = 0.0

    def get_width_height(self) -> tuple[float, float]:
        """Retorna a largura e a altura da janela de visualização. (Wx, Wy)"""

        return (
            self.window_bounds.x_max - self.window_bounds.x_min,
            self.window_bounds.y_max - self.window_bounds.y_min,
        )

    def apply_zoom(self, zoom_level: float) -> None:
        """Aplica um zoom na janela de visualização baseado no nível de zoom."""

        zoom_level /= 100

        relative_change = zoom_level / self.zoom_level
        self.zoom_level = zoom_level

        scaling_factor = 1 / relative_change

        self.window_bounds.x_min *= scaling_factor
        self.window_bounds.x_max *= scaling_factor
        self.window_bounds.y_min *= scaling_factor
        self.window_bounds.y_max *= scaling_factor

    def apply_pan(self, d_vertical, d_horizontal: float, d_depth: float) -> None:
        """
        Aplica um pan na janela de visualização.
        @param d_vertical: Deslocamento vertical
        @param d_horizontal: Deslocamento horizontal
        @param d_depth: Deslocamento em profundidade
        """

        pan_mtx = TransformationGenerator.get_pan_matrix(
            d_vertical,
            d_horizontal,
            d_depth,
            self.vup,
            self.vright,
            self.view_plane_normal,
        )

        self.window_center = self.window_center @ pan_mtx

        min_point = np.array(
            [self.window_bounds.x_min, self.window_bounds.y_min, 0.0, 1.0]
        )
        min_point = min_point @ pan_mtx
        self.window_bounds.x_min = min_point[0]
        self.window_bounds.y_min = min_point[1]

        max_point = np.array(
            [self.window_bounds.x_max, self.window_bounds.y_max, 0.0, 1.0]
        )
        max_point = max_point @ pan_mtx
        self.window_bounds.x_max = max_point[0]
        self.window_bounds.y_max = max_point[1]

    def apply_rotation(self, angle_degrees: float) -> None:
        """Aplica uma rotação na janela de visualização."""

        self.angle = np.radians(angle_degrees)

        # Rotaciona o vup para o novo ângulo
        rotation_matrix = np.array(
            [
                [np.cos(self.angle), -np.sin(self.angle)],
                [np.sin(self.angle), np.cos(self.angle)],
            ]
        )

        self.vup = rotation_matrix @ np.array([0.0, 1.0])
