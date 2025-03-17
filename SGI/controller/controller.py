from view.view import View


class Controller:
    """Classe que representa o controller da nossa arquitetura MVC."""

    def __init__(self):
        self.view = View(controller=self)

    def run(self):
        """Executa a aplicação."""
        self.view.root.mainloop()

    def handle_coordinate_input(self, coordinate_input: str):  # TODO
        """Recebe e lida com a entrada do usuário contendo as coordenadas dos pontos."""

        try:
            points = list(eval(coordinate_input))
        except Exception as e:
            pass
