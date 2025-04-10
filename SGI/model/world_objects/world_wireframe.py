from model.world_objects.world_object import WorldObject
from view.graphical_objects.graphical_object import GraphicalObject
from view.graphical_objects.graphical_wireframe import GraphicalWireframe


class WorldWireframe(WorldObject):
    """Classe pertinente a wireframes no mundo."""

    def get_clipped_representation(self) -> None:
        graphical_wireframe = GraphicalWireframe(self.viewport_points, self.color)
        return [graphical_wireframe]
