import logging

from model.model import Model
from view.view import View


class Controller:
    """Classe que representa o controller da nossa arquitetura MVC."""

    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format="\033[94m[%(levelname)s] %(filename)s:%(lineno)d - %(message)s\033[0m",
        )

        self.view = View(controller=self)
        self.model = Model(view=self.view)

    def run(self) -> None:
        """Executa a aplicação."""
        self.view.root.mainloop()

    def handle_point_input(self, points_input: str, name_input: str) -> None:  # TODO
        """Recebe e lida com a entrada do usuário contendo as coordenadas dos pontos."""

        try:
            points = list(eval(points_input))
            self.model.add_object(points, name_input)
        except NameError as e:
            logging.debug(f"Erro ao converter coordenadas: {e}", exc_info=True)
