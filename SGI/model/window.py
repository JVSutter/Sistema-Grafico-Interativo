import logging
from view.bounds import Bounds

class Window:
    """Classe que representa a Window (janela de visualização) do mundo."""

    def __init__(self):
        # Valores iniciais da window
        self._x_min = -100.0
        self._y_min = -100.0
        self._x_max = 100.0
        self._y_max = 100.0
        
        # Fatores de zoom e pan
        self._zoom_factor = 1.0
        
    @property
    def zoom_factor(self):
        """Getter para o fator de zoom."""
        return self._zoom_factor
        
    @zoom_factor.setter
    def zoom_factor(self, value):
        """Setter para o fator de zoom."""
        self._zoom_factor = value
        
    def get_bounds(self) -> Bounds:
        """Retorna os limites atuais da window."""
        return Bounds(
            x_min=self._x_min,
            y_min=self._y_min,
            x_max=self._x_max,
            y_max=self._y_max
        )
    
    def zoom(self, factor):
        """Aplica zoom na window."""
        # Calcula o centro atual da window
        center_x = (self._x_min + self._x_max) / 2
        center_y = (self._y_min + self._y_max) / 2
        
        # Calcula a metade da largura e altura
        half_width = (self._x_max - self._x_min) / 2
        half_height = (self._y_max - self._y_min) / 2
        
        # Aplica o fator de zoom às dimensões
        new_half_width = half_width / factor
        new_half_height = half_height / factor
        
        # Recalcula os limites mantendo o centro
        self._x_min = center_x - new_half_width
        self._x_max = center_x + new_half_width
        self._y_min = center_y - new_half_height
        self._y_max = center_y + new_half_height
        
        logging.info(f"Zoom aplicado: fator {factor}. Novos limites: ({self._x_min}, {self._y_min}) a ({self._x_max}, {self._y_max})")
    
    def pan(self, direction, amount=10.0):
        """Aplica panning na window."""
        width = self._x_max - self._x_min
        height = self._y_max - self._y_min
        
        # Ajusta a quantidade de pan com base no tamanho da window
        pan_amount_x = width * 0.05 * amount / 10.0
        pan_amount_y = height * 0.05 * amount / 10.0
        
        if direction == "up":
            self._y_min += pan_amount_y
            self._y_max += pan_amount_y
        elif direction == "down":
            self._y_min -= pan_amount_y
            self._y_max -= pan_amount_y
        elif direction == "left":
            self._x_min -= pan_amount_x
            self._x_max -= pan_amount_x
        elif direction == "right":
            self._x_min += pan_amount_x
            self._x_max += pan_amount_x
            
        logging.info(f"Pan aplicado: direção {direction}. Novos limites: ({self._x_min}, {self._y_min}) a ({self._x_max}, {self._y_max})")
