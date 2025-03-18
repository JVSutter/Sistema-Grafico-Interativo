import tkinter as tk

from view.bounds import Bounds


class View:
    """Classe que representa a view da nossa arquitetura MVC."""

    def __init__(self, controller):
        self.controller = controller
        self.create_interface()

    def create_interface(self) -> None:
        """Cria e inicializa a interface gráfica do programa"""

        self.root = tk.Tk()
        self.root.title("Sistema Gráfico Interativo")

        # Frame superior (divide em esquerdo e direito)
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Painel esquerdo para botões de zoom e navegação
        left_panel = tk.Frame(top_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        tk.Button(left_panel, text="Zoom In").pack(pady=2)
        tk.Button(left_panel, text="Zoom Out").pack(pady=2)
        tk.Button(left_panel, text="↑").pack(pady=2)
        tk.Button(left_panel, text="↓").pack(pady=2)
        tk.Button(left_panel, text="←").pack(pady=2)
        tk.Button(left_panel, text="→").pack(pady=2)
        tk.Button(
            left_panel, text="Criar objeto", command=self.on_object_creation
        ).pack(pady=2)

        # Painel direito para o viewport
        right_panel = tk.Frame(top_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(right_panel, width=500, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.window = Bounds(x_min=-100, x_max=100, y_min=-100, y_max=100)
        self.viewport = Bounds(x_min=0, x_max=500, y_min=0, y_max=500)

    def on_object_creation(self) -> None:
        """Exibe uma caixa de diálogo para criação de um objeto."""

        dialog = tk.Toplevel(self.root)
        dialog.title("Criar objeto")

        tk.Label(
            dialog,
            text="Insira as coordenadas dos pontos\nFormato esperado: (x1, y1),(x2, y2),...",
        ).pack()
        points_entry = tk.Entry(dialog)
        points_entry.pack()

        tk.Label(dialog, text="Insira o nome do objeto").pack()
        name_entry = tk.Entry(dialog)
        name_entry.pack()

        def on_ok() -> None:
            points_input = points_entry.get()
            name_input = name_entry.get()
            dialog.destroy()
            self.controller.handle_point_input(points_input, name_input)

        tk.Button(dialog, text="Ok", command=on_ok).pack()

    def draw_object(self, points: list) -> None:  # NÃO CONECTA OS PONTOS AINDA
        """Desenha um objeto gráfico na tela."""

        for point in points:
            x, y = point
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
