from dataclasses import dataclass


@dataclass
class WindowBounds:
    """
    Classe para armazenar os limites da Window: canto inferior esquerdo e canto superior direito.
    (left, down, z_min) é o canto inferior esquerdo da janela
    (right, up, z_max) é o canto superior direito da janela
    """

    x_lower_left: float
    y_lower_left: float
    z_lower_left: float
    x_upper_right: float
    y_upper_right: float
    z_upper_right: float
