from dataclasses import dataclass


@dataclass
class Bounds:
    """Classe para armazenar os limites de uma área retangular."""

    x_min: float
    x_max: float
    y_min: float
    y_max: float
    # Opcionalmente, podemos adicionar limites para o eixo Z
    z_min: float = 0.0
    z_max: float = 0.0
