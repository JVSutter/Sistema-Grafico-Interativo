import numpy as np

from model.world_objects.world_curve import WorldCurve


class WorldBSplineCurve(WorldCurve):
    """
    Classe pertinente a curvas B-spline no mundo.
    """

    def _generate_curve_points_normalized(self) -> list[tuple[float, float]]:
        """
        Gera pontos ao longo da curva B-spline usando a forma matricial em coordenadas normalizadas.
        @return: Lista de pontos (x, y) normalizados ao longo da curva.
        """

        #  TODO: Implementar geração de pontos com forward differences
