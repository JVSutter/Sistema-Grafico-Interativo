import numpy as np

from model.model import Model
from view.view import View


class Controller:
    """
    Classe que representa o controller da nossa arquitetura MVC.
    Métodos handle_* são chamados pela View para processar entradas do usuário.
    """

    def __init__(self):
        self.view = View(controller=self)
        self.model = Model(view=self.view)

    def run(self) -> None:
        """Executa a aplicação."""

        self.view.run()

    def handle_create_object(
        self,
        points_input: list,
        name_input: str,
        color_input: tuple,
        is_filled: bool,
        object_type: str,
    ) -> None:
        """
        Constrói um novo objeto no mundo.
        @param points_input: Lista de pontos que compõem o objeto.
        @param name_input: Nome do objeto
        @param color_input: Cor do objeto
        @param is_filled: Se o objeto é preenchido ou não
        @param object_type: Tipo de objeto
        """

        # self.model.add_object(
        #     points=points_input,
        #     name=name_input,
        #     color=color_input,
        #     is_filled=is_filled,
        #     object_type=object_type,
        # )

        print("TODO: handle_create_object")

    def handle_remove_object(self, index: int) -> None:
        """
        Remove um objeto do mundo.
        @param index: Índice do objeto a ser removido.
        """

        # self.model.remove_object(index=index)
        print("TODO: handle_remove_object")

    def handle_zoom(self, new_zoom_value: float) -> None:
        """
        Processa um zoom out/in da janela de visualização.
        @param new_zoom_value: Novo valor de zoom.
        """

        # self.model.zoom(new_zoom_value)
        print("TODO: handle_zoom")

    def handle_pan(self, dx: float, dy: float) -> None:
        """
        Processa um deslocamento na janela de visualização.
        @param dx: Deslocamento em x.
        @param dy: Deslocamento em y.
        """

        # self.model.pan(dx, dy)
        print("TODO: handle_pan")

    def handle_transformations(
        self, index: int, transformations_list: list[dict]
    ) -> None:
        """
        Processa uma lista de transformações aplicadas a um objeto.
        @param index: Índice do objeto a ser transformado.
        @param transformations_list: Lista de transformações a serem aplicadas.
        """

        # self.model.handle_transformations(index, transformations_list)
        print("TODO: handle_transformations")

    def handle_window_rotation(self, angle: float) -> None:
        """
        Processa uma rotação da janela de visualização.
        @param angle: Ângulo de rotação.
        """

        # self.model.rotate_window(angle)
        print("TODO: handle_window_rotation")

    def handle_import_obj_file(self, filepath: str) -> None:
        """
        Importa um arquivo .obj.
        @param filepath: Caminho do arquivo .obj.
        """

        # self.model.import_obj_file(filepath)
        print("TODO: handle_import_obj_file")

    def handle_export_obj_file(self, filepath: str) -> None:
        """
        Exporta um arquivo .obj.
        @param filepath: Caminho do arquivo .obj.
        """

        # self.model.export_obj_file(filepath)
        print("TODO: handle_export_obj_file")

    def handle_clipping_change(self, mode: str) -> None:
        """
        Muda o modo de clipping.
        @param mode: Modo de clipping.
        """

        # self.model.change_clipping_mode(mode)
        print("TODO: handle_clipping_change")

    def handle_add_test_objects(self) -> None:
        """Adiciona objetos de teste ao mundo."""

        # self.model.add_test_objects()
        print("TODO: handle_add_test_objects")

    def handle_remove_test_objects(self) -> None:
        """Remove objetos de teste do mundo."""

        # self.model.remove_test_objects()
        print("TODO: handle_remove_test_objects")
