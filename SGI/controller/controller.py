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
        """
        Recebe e lida com a entrada do usuário contendo as coordenadas dos pontos.
        @param points_input: Lista de pontos que compõem o objeto.
        @param name_input: Nome do objeto
        """

        self.model.add_object(points=points_input, name=name_input)

    def handle_remove_object(self, index: int) -> None:
        """
        Lida com as requisições de remoção de objeto vindas do View.
        @param index: Índice do objeto a ser removido.
        """
        self.model.remove_object(index=index)

    def handle_zoom(self, factor: float) -> None:
        """
        Lida com as requisições de zoom vindas do View.
        @param factor: Fator de zoom.
        """
        self.model.zoom(factor)

    def handle_pan(self, dx: float, dy: float) -> None:
        """
        Lida com as requisições de pan vindas do View.
        @param dx: Deslocamento em x.
        @param dy: Deslocamento em y.
        """

        self.model.pan(dx, dy)

    def handle_transformation(self, index: int, transformation_info: dict) -> None:
        """
        Lida com as requisições de transformação de objeto vindas do View.
        @param index: Índice do objeto a ser transformado.
        @param transformation_info: Informações da transformação a ser aplicada.
        """

        if transformation_info is None:
            return

        transformation_option = transformation_info["option"]
        x_value = transformation_info["x_value"]
        y_value = transformation_info["y_value"]
        angle = transformation_info.get("angle", None)

        if transformation_option == "translation":
            self.model.translate_object(index, x_value, y_value)
        elif transformation_option == "scaling":
            self.model.scale_object(index, x_value, y_value)
        elif transformation_option == "rotation":
            self.model.rotate_object(index, x_value, y_value, angle)
