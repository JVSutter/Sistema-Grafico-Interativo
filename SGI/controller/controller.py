from view.view import View


class Controller:
    """Classe que representa o controller da nossa arquitetura MVC."""

    def __init__(self):
        self.view = View(controller=self)

    def run(self):
        """Executa a aplicação."""
        self.view.root.mainloop()

    def on_create_object(self)