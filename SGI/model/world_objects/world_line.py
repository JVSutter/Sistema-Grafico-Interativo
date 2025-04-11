from model.world_objects.world_object import WorldObject
from view.graphical_objects.graphical_line import GraphicalLine


class WorldLine(WorldObject):
    """Classe pertinente a linhas no mundo."""

    def get_clipped_representation(self) -> None:  # TODO
        graphical_line = GraphicalLine(self.viewport_points, self.color)
        return [graphical_line]
