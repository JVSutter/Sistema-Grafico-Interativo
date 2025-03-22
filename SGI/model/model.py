import logging

from model.graphical_object import GraphicalObject
from model.window import Window
from view.bounds import Bounds


class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view):
        self.view = view
        self._display_file = []
        self.window = Window()

    def add_object(self, points: list, name: str) -> None:
        """Adiciona um objeto gráfico ao display file."""
        graphical_object = GraphicalObject(points=points, name=name)
        self._display_file.append(graphical_object)

        logging.info(f"Objeto {graphical_object} adicionado ao display file.")
        self.view.update_viewport()
        
    def get_display_file(self):
        """Retorna a lista de objetos gráficos."""
        return self._display_file
        
    def remove_object(self, index):
        """Remove um objeto pelo índice."""
        if 0 <= index < len(self._display_file):
            removed = self._display_file.pop(index)
            logging.info(f"Objeto {removed} removido do display file.")
            self.view.update_viewport()
        
    def get_window_bounds(self) -> Bounds:
        """Retorna os limites da window atual."""
        return self.window.get_bounds()
    
    def zoom(self, factor):
        """Aplica zoom na window."""
        self.window.zoom(factor)
        self.view.update_viewport()
        
    def pan(self, direction):
        """Aplica panning na window."""
        self.window.pan(direction)
        self.view.update_viewport()
