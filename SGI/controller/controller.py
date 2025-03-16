from view.view import View


class Controller:
    """Classe que representa o controller da nossa arquitetura MVC."""

    def __init__(self):
        self.view = View()

    def run(self):
        """Executa a aplicação."""
        self.view.root.mainloop()
