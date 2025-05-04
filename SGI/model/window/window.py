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
        self.view_plane_normal = np.array([0.0, 0.0, 1.0, 1.0])

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
        self.angle_horizontal = 0.0
        self.angle_vertical = 0.0
        self.angle_spin = 0.0

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

    def apply_rotation(self, angle_degrees: float, axis: str) -> None:
        """
        Aplica uma rotação na janela de visualização. O algoritmo funciona da seguinte forma:
        1 - A rotação será ou em torno do eixo horizontal, vertical ou em torno de si mesma (eixo que perfura a window).
        Logo, a direção do eixo será a mesma do vetor vup, do vright ou do vpn, dependendo do tipo de rotação.
        Portanto, precisamos "copiar" o vetor correspondente e fazer a cópia passar pelo centro da janela. Isto requer
        uma translação.
        2 - Quando o eixo estiver na posição certa, aplicamos a rotação em torno dele.
        3 - Por fim, atualizamos os bounds e também os vetores de direção (pois dois deles vão mudar de direção).
        @param angle_degrees: Ângulo final da rotação
        @param axis: Eixo de rotação
        """

        print(f"window center before: {self.window_center}")

        axis_vector = {
            "horizontal": self.vup,
            "vertical": self.vright,
            "spin": self.view_plane_normal,
        }.get(axis)

        if axis_vector is None:
            return

        angle_attr = f"angle_{axis}"
        angle_delta = angle_degrees - getattr(self, angle_attr)
        setattr(self, angle_attr, angle_degrees)

        p1 = self.window_center[::]
        p2 = [
            self.window_center[0] + axis_vector[0],
            self.window_center[1] + axis_vector[1],
            self.window_center[2] + axis_vector[2],
            1.0,
        ]

        print(f"p1: {p1}, p2: {p2}")

        rotation_matrix = TransformationGenerator.get_arbitrary_rotation_matrix(
            angle_degrees=angle_delta,
            p1=p1,
            p2=p2,
        )

        self.window_bounds.lower_left_point = (
            self.window_bounds.lower_left_point @ rotation_matrix
        )
        self.window_bounds.upper_right_point = (
            self.window_bounds.upper_right_point @ rotation_matrix
        )

        # Os vetores de direção também precisam ser rotacionados, mas não ao redor do eixo
        # que foi escolhido para a rotação. Eles devem ser rotacionados em torno do eixo
        # de direção de referência.
        direction_vectors_rotation_axis = [
            (0, 0, 0, 1),
            (axis_vector[0], axis_vector[1], axis_vector[2], 1),
        ]
        direction_vectors_rotation_matrix = (
            TransformationGenerator.get_arbitrary_rotation_matrix(
                angle_degrees=angle_delta,
                p1=direction_vectors_rotation_axis[0],
                p2=direction_vectors_rotation_axis[1],
            )
        )

        if not np.array_equal(self.vup, axis_vector):
            self.vup = self.vup @ direction_vectors_rotation_matrix

        if not np.array_equal(self.vright, axis_vector):
            self.vright = self.vright @ direction_vectors_rotation_matrix

        if not np.array_equal(self.view_plane_normal, axis_vector):
            self.view_plane_normal = (
                self.view_plane_normal @ direction_vectors_rotation_matrix
            )

        print("view_plane_normal:", self.view_plane_normal)
        print("vup:", self.vup)
        print("vright:", self.vright)
        print("window_bounds:", self.window_bounds)
        print("window_center:", self.window_center)

    def get_width(self) -> float:
        """Retorna a largura da janela de visualização."""
        return self.window_bounds.x_upper_right - self.window_bounds.x_lower_left

    def get_height(self) -> float:
        """Retorna a altura da janela de visualização."""
        return self.window_bounds.y_upper_right - self.window_bounds.y_lower_left
