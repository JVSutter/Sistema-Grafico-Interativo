from model.graphical_algorithms import GraphicalAlgorithms
from model.world_objects.world_object import WorldObject
from view.graphical_objects.graphical_line import GraphicalLine


class WorldLine(WorldObject):
    """Classe pertinente a linhas no mundo."""

    def get_clipped_representation(self) -> None:
        p1 = self.normalized_points[0]
        p2 = self.normalized_points[1]

        clipped_points = GraphicalAlgorithms.cohen_sutherland_clipping(p1, p2)

        if clipped_points is None:
            return []

        viewport_points = self.transform_normalized_points_to_viewport(clipped_points)
        graphical_representation = GraphicalLine(viewport_points, self.color)
        return graphical_representation
