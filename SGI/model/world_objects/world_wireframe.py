from model.graphical_algorithms import GraphicalAlgorithms
from model.world_objects.world_object import WorldObject
from view.graphical_objects.graphical_wireframe import GraphicalWireframe


class WorldWireframe(WorldObject):
    """Classe pertinente a wireframes no mundo."""

    def get_clipped_representation(self) -> None:
        clipped_points = GraphicalAlgorithms.sutherland_hodgman_clipping(
            self.normalized_points
        )
        if not clipped_points:
            return []

        viewport_points = self.transform_normalized_points_to_viewport(clipped_points)
        graphical_representation = GraphicalWireframe(viewport_points, self.color)
        return [graphical_representation]
