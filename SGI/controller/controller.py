import tkinter as tk
from view.window import Window
from view.viewport import Viewport


class Controller:
    """Classe que representa o controller da nossa arquitetura MVC."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Gráfico Interativo")

        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.window = Window(x_min=-100, x_max=-100, y_min=100, y_max=100)
        self.viewport = Viewport(x_min=0, x_max=500, y_min=0, y_max=500)

    def run(self):
        """Executa a aplicação."""
        self.root.mainloop()
