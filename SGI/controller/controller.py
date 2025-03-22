import logging

from model.model import Model
from view.view import View


class Controller:
    """Classe que representa o controller da nossa arquitetura MVC."""

    def __init__(self):
        self._setup_logging()
        self.view = View(controller=self)
        self.model = Model(view=self.view)

    def _setup_logging(self):
        """Configura o sistema de logging."""
        logging.basicConfig(
            level=logging.DEBUG,
            format="\033[94m[%(levelname)s] %(filename)s:%(lineno)d - %(message)s\033[0m",
        )

    def run(self) -> None:
        """Executa a aplicação."""
        self.view.run()

    def handle_object_creation(self, points_input: list, name_input: str) -> None:
        """Recebe e lida com a entrada do usuário para criar um objeto."""
        self.model.add_object(points=points_input, name=name_input)
        
    def get_object_strings(self):
        """Obtém a lista de strings representando os objetos para exibição na listview."""
        return [str(obj) for obj in self.model.get_display_file()]
    
    def get_objects(self):
        """Obtém a lista de objetos gráficos."""
        return self.model.get_display_file()
    
    def remove_object(self, index):
        """Remove um objeto pelo índice."""
        self.model.remove_object(index)
        
    def handle_zoom(self, factor):
        """Lida com requisição de zoom."""
        self.model.zoom(factor)
        
    def handle_pan(self, direction):
        """Lida com requisição de panning."""
        self.model.pan(direction)
        
    def get_window_bounds(self):
        """Obtém os limites da window atual."""
        return self.model.get_window_bounds()
