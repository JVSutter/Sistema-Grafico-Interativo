from model.world_object import WorldObject
from view.view import View


class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view: View):
        self.view = view
        self.display_file = []

    def add_object(self, points: list, name: str) -> None:
        """Adiciona um objeto gráfico ao display file e atualiza a View."""

        window_bounds = self.view.viewport.window_bounds
        viewport_bounds = self.view.viewport.viewport_bounds
        graphical_object = WorldObject(points, name, window_bounds, viewport_bounds)

        self.display_file.append(graphical_object)
        self.view.update_object_list(self.get_object_list())
        self.view.update_viewport([obj.graphical_representation for obj in self.display_file])

    def get_object_list(self):
        """Retorna uma representação em string dos objetos do mundo."""
        return [str(obj) for obj in self.display_file]
