from dataclasses import dataclass


@dataclass
class Bounds:
    """Classe para armazenar os limites de um elemento gráfico."""

    x_min: float
    x_max: float
    y_min: float
    y_max: float
