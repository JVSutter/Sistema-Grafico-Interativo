from abc import ABC, abstractmethod

import numpy as np

from utils.bounds import Bounds


class WorldObject(ABC):
    """Classe pertinente a objetos pertencentes ao modelo interno (mundo)."""

    def __init__(
        self,
        points: list,
        name: str,
        color: tuple[int, int, int],
        viewport_bounds: Bounds,
    ):

        self.world_points: list[np.array] = self.get_homogeneous_coordinates(points)
        self.normalized_points: list[tuple[float, float]] = []
        self.viewport_points: list[tuple[float, float]] = []
        self.viewport_bounds: Bounds = viewport_bounds

        self.name = name
        self.color = color

    def update_normalized_points(self, norm_points: list[tuple[float, float]]):
        """Atualiza as coordenadas normalizadas (NCS)"""

        self.normalized_points = norm_points
        self.viewport_points = self.transform_normalized_points_to_viewport()

    @abstractmethod
    def get_clipped_representation(self) -> None:
        """
        Executa algoritmos de clipping para o objeto antes de passar a representação gráfica para
        o viewport.

        @param representation_list: lista de objetos gráficos a serem desenhados no Viewport. Um mesmo objeto pode
        apendar zero, uma ou mais representações gráficas, dependendo do resultado do clipping.
        """

    def transform_normalized_points_to_viewport(self) -> list[tuple[float, float]]:
        """Retorna as coordenadas do objeto gráfico para o viewport."""

        transformed_points = []
        for point in self.normalized_points:
            nx, ny = point

            vp_width = self.viewport_bounds.x_max - self.viewport_bounds.x_min
            vp_height = self.viewport_bounds.y_max - self.viewport_bounds.y_min

            vx = (nx + 1) / 2 * vp_width + self.viewport_bounds.x_min
            vy = (1 - ny) / 2 * vp_height + self.viewport_bounds.y_min
            transformed_points.append((vx, vy))

        return transformed_points

    def get_homogeneous_coordinates(self, points: list[tuple]) -> list[np.array]:
        """Retorna as coordenadas homogêneas dos pontos do objeto."""

        homogeneous_coordinates = []
        for point in points:
            x, y = point
            homogeneous_coordinates.append(np.array([x, y, 1]))
        return homogeneous_coordinates

    def update_coordinates(self, composite_matrix: np.ndarray) -> None:
        """
        Atualiza as coordenadas do objeto no mundo aplicando uma matriz de transformação composta.
        """
        self.world_points = [point @ composite_matrix for point in self.world_points]

    def get_center(self) -> tuple[float, float]:
        """Retorna o centro geométrico do objeto no mundo."""

        x_sum = sum(point[0] for point in self.world_points)
        y_sum = sum(point[1] for point in self.world_points)
        x_center = x_sum / len(self.world_points)
        y_center = y_sum / len(self.world_points)

        return x_center, y_center

    def get_obj_description(self) -> None:
        """Retorna a descrição do objeto em formato .obj"""

        obj_description = ""

        for point in self.world_points:
            obj_description += f"v {point[0]:.1f} {point[1]:.1f}\n"

        obj_description += f"o {self.name}\n"

        if len(self.world_points) == 1:
            obj_type = "p"
        elif len(self.world_points) == 2:
            obj_type = "l"
        else:
            obj_type = "f"

        obj_description += f"{obj_type} {" ".join(str(i) for i in range(-1, -len(self.world_points) - 1, -1))}\n\n"

        return obj_description

    def __str__(self):
        formatted_points = ", ".join(
            f"({x:.1f}, {y:.1f})" for x, y, _ in self.world_points
        )
        return f"{self.__class__.__name__.replace("World", "")} {self.name}: {formatted_points}"
