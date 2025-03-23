from model.model import Model
from view.view import View


class Controller:
    """Classe que representa o controller da nossa arquitetura MVC."""

    def __init__(self):
        self.view = View(controller=self)
        self.model = Model(view=self.view)

    def run(self) -> None:
        """Executa a aplicação."""
        self.view.run()

    def handle_point_input(self, points_input: list, name_input: str) -> None:
        """Recebe e lida com a entrada do usuário contendo as coordenadas dos pontos."""
        self.model.add_object(points=points_input, name=name_input)

    def remove_object(self, index: int) -> None:
        """Remove um objeto da lista de objetos."""
        self.model.remove_object(index=index)
