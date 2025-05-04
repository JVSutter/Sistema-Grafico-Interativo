import numpy as np

from model.transformation_generator import TransformationGenerator
from model.window.window_bounds import WindowBounds
from view.viewport.viewport_bounds import ViewportBounds


class Window:
    """Classe que representa a janela de visualização."""

    def __init__(self, viewport_bounds: ViewportBounds):
        """
        Como o tamanho do viewport é determinado em tempo de execução,
        adequamos o tamanho da janela de visualização para manter a proporção. De
        outra forma, a imagem seria distorcida.
        """

        viewport_width = viewport_bounds.x_lower_right - viewport_bounds.x_upper_left
        viewport_height = viewport_bounds.y_lower_right - viewport_bounds.y_upper_left
        aspect_ratio = viewport_width / viewport_height

        # O centro da Window foi escolhido como o VRP (View Reference Point) por conveniência
        self.window_center = np.array([0.0, 0.0, 0.0, 1.0])

        # Vetores da window: um apontando pra cima, um apontando pra direita e um apontando pra frente
        # Window começa sobre o plano xy, olhando em direção a z positivo
        # O eixo y indica a direção "cima", e o eixo "x" aponta para a esquerda
        self.vup = np.array([0.0, 1.0, 0.0, 1.0])
        self.vright = np.array([-1.0, 0.0, 0.0, 1.0])
        self.view_plane_normal = np.array(
            [0.0, 0.0, 1.0, 1.0]
        )

        height = 20  # Valor default
        width = height * aspect_ratio

        self.window_bounds = WindowBounds(
            x_lower_left=width,
            x_upper_right=-width,
            y_lower_left=-height,
            y_upper_right=height,
            z_lower_left=0.0,
            z_upper_right=0.0,
        )

        self.zoom_level = 1.0
        self.angle = 0.0

    def apply_zoom(self, zoom_level: float) -> None:
        """Aplica um zoom na janela de visualização baseado no nível de zoom."""

        zoom_level /= 100

        relative_change = zoom_level / self.zoom_level
        self.zoom_level = zoom_level
        scaling_factor = 1 / relative_change

        cx, cy, cz, _ = self.window_center
        scaling_matrix = TransformationGenerator.get_scaling_matrix(
            scale_x=scaling_factor,
            scale_y=scaling_factor,
            scale_z=scaling_factor,
            cx=cx,
            cy=cy,
            cz=cz,
        )

        self.window_center = self.window_center @ scaling_matrix

        self.window_bounds.upper_right_point = (
            self.window_bounds.upper_right_point @ scaling_matrix
        )
        self.window_bounds.lower_left_point = (
            self.window_bounds.lower_left_point @ scaling_matrix
        )

    def apply_pan(self, d_horizontal: float, d_vertical: float, d_depth: float) -> None:
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
        self.window_bounds.upper_right_point = (
            self.window_bounds.upper_right_point @ pan_mtx
        )
        self.window_bounds.lower_left_point = (
            self.window_bounds.lower_left_point @ pan_mtx
        )

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

    def get_width(self) -> float:
        """Retorna a largura da janela de visualização."""
        return self.window_bounds.x_upper_right - self.window_bounds.x_lower_left

    def get_height(self) -> float:
        """Retorna a altura da janela de visualização."""
        return self.window_bounds.y_upper_right - self.window_bounds.y_lower_left
