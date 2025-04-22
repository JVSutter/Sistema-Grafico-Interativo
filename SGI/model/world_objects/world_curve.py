from abc import ABC, abstractmethod

from model.clipping_algorithms import ClippingAlgorithms
from model.world_objects.sc_world_object import SCWorldObject
from view.graphical_objects.graphical_curve import GraphicalCurve


class WorldCurve(SCWorldObject, ABC):
    """Classe pertinente a curvas no mundo."""

    def __init__(self, points, name, color, viewport_bounds):
        super().__init__(points, name, color, viewport_bounds)

        self.clipping_mode = ClippingAlgorithms.cohen_sutherland_clipping
        self.clipping_modes = {
            "cohen_sutherland": ClippingAlgorithms.cohen_sutherland_clipping,
            "liang_barsky": ClippingAlgorithms.liang_barsky_clipping,
        }

    def update_normalized_points(self, norm_points: list[tuple[float, float]]):
        """
        Atualiza as coordenadas normalizadas (NCS) dos pontos de controle do objeto
        e recalcula os pontos da curva para o viewport.
        @param norm_points: Lista de pontos de controle normalizados.
        """

        self.normalized_points = norm_points
        self.curve_points = self._generate_curve_points_normalized()
        self.viewport_points = self.transform_normalized_points_to_viewport(
            self.curve_points
        )

    @abstractmethod
    def _generate_curve_points_normalized(self) -> list[tuple[float, float]]:
        """
        Gera pontos ao longo da curva usando a forma matricial em coordenadas normalizadas.
        @return: Lista de pontos (x, y) normalizados ao longo da curva.
        """

    def get_clipped_representation(self) -> list:
        """
        Retorna a representação gráfica da curva após dividir em retas e aplicar clipping.
        """

        clipped_parts = ClippingAlgorithms.curve_clipping(
            self.curve_points, self.clipping_mode
        )
        if not clipped_parts:
            return []

        representations = []

        for part in clipped_parts:
            viewport_points = self.transform_normalized_points_to_viewport(part)

            representations.append(
                GraphicalCurve(
                    viewport_points,
                    self.color,
                )
            )

        return representations
