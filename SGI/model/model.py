import os

from model.display_file_manager import DisplayFileManager
from model.window import Window
from view.graphical_objects.graphical_object import GraphicalObject
from view.view import View


class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view: View):
        self.view = view
        self.window = Window(viewport_bounds=view.viewport.viewport_bounds)
        self.display_file_manager = DisplayFileManager(
            self.view.viewport.viewport_bounds
        )

    @staticmethod
    def update_interface(func: callable) -> callable:
        """Decorator para atualizar a interface quando uma função é chamada."""

        def wrapper(*args, **kwargs):
            self = args[0]
            result = func(*args, **kwargs)

            # Recalcula as coordenadas normalizadas para todos os objetos
            self._calculate_and_update_ncs()

            # Atualiza a View
            graphical_representations = self.get_graphical_representations()
            obj_list = self.display_file_manager.get_objs_as_strings()
            self.view.update_view_objects(graphical_representations, obj_list)

            return result

        return wrapper

    def get_graphical_representations(self) -> list[GraphicalObject]:
        """
        Retorna as representações gráficas de todos os objetos gráficos a serem mostrados no Viewport
        """

        return self.display_file_manager.get_clipped_representations()

    @update_interface
    def add_object(self, points: list, name: str, color: tuple) -> None:
        """Adiciona um objeto gráfico ao mundo."""

        if self.display_file_manager.add_object(points=points, name=name, color=color):
            self.view.add_log(f"Object {name} added: {points}")
            return

        self.view.add_log("Object already exists, skipping...")

    @update_interface
    def remove_object(self, index: int) -> None:
        """
        Remove um objeto do display file e atualiza a View.
        @param index: Índice do objeto a ser removido. Coincide com o índice na lista de objetos da interface.
        """

        self.display_file_manager.remove_object(index)

    @update_interface
    def zoom(self, factor: float) -> None:
        """
        Aplica um zoom na janela de visualização e atualiza a View.
        @factor: Fator de zoom. Valores maiores que 1 aumentam o zoom, valores menores que 1 diminuem.
        """
        self.window.apply_zoom(factor)

    @update_interface
    def pan(self, dx: float, dy: float) -> None:
        """Aplica um pan na janela de visualização e atualiza a View.
        @param dx: Deslocamento em x.
        @param dy: Deslocamento em y.
        """
        self.window.apply_pan(dx, dy)

    @update_interface
    def handle_transformations(
        self,
        index: int,
        transformations_list: list[dict],
    ) -> None:
        """
        Processa uma lista de transformações em um objeto sequencialmente,
        compondo uma matriz única e aplicando-a ao final.
        @param index: Índice do objeto a ser transformado.
        @param transformations_list: Lista de dicionários, cada um representando uma transformação.
        """

        for transformation in transformations_list:
            if transformation["type"] == "scale":
                self.view.add_log(
                    f"Scaling object {index} by factors {transformation['sx']}, {transformation['sy']}"
                )
            elif transformation["type"] == "translate":
                self.view.add_log(
                    f"Translating object {index} by ({transformation['dx']}, {transformation['dy']})"
                )
            elif transformation["type"] == "rotate":
                self.view.add_log(
                    f"Rotating object {index} by {transformation['angle']} degrees"
                )

        obj = self.display_file_manager.display_file[index]
        self.view.add_log(f"{obj.name}: Transformations applied.")

    def _calculate_and_update_ncs(self) -> None:
        """Calcula as coordenadas normalizadas para todos os objetos."""

        window_cx, window_cy = self.window.get_center()
        window_width, window_height = self.window.get_width_height()
        window_vup = self.window.vup

        self.display_file_manager.update_ncs_coordinates(
            window_cx=window_cx,
            window_cy=window_cy,
            window_height=window_height,
            window_width=window_width,
            window_vup=window_vup,
        )

    @update_interface
    def import_obj_file(self, filepath: str) -> None:
        """
        Importa um arquivo .obj para o display file.
        @param filepath: Caminho do arquivo .obj a ser importado.
        """

        try:
            world_objects, skipped_objects = (
                self.display_file_manager.import_file_to_display_file(filepath=filepath)
            )

            for world_object in world_objects:
                self.view.add_log(
                    f"Object {world_object.name} imported: {world_object.world_points}"
                )
            if skipped_objects:
                self.view.add_log(f"Skipped objects: {skipped_objects}")

        except FileNotFoundError:
            self.view.add_log(f"File not found: {filepath}")
            return
        except Exception as e:
            self.view.add_log(f"Error importing file: {e}")
            return

    def export_obj_file(self, filepath: str, name: str) -> None:
        """
        Exporta os objetos do display file para um arquivo .obj.
        @param filepath: Caminho do diretório onde o arquivo .obj será salvo.
        @param name: Nome do arquivo .obj a ser salvo.
        """

        if not name:
            name = "output"

        filepath = os.path.join(filepath, f"{name}.obj")
        obj_str = self.display_file_manager.convert_display_file_to_obj()

        with open(filepath, "w") as f:
            f.write(obj_str)

        self.view.add_log(f"Objects successfully exported to {filepath}")

    @update_interface
    def rotate_window(self, angle: float) -> None:
        """
        Rotaciona a janela de visualização para o ângulo especificado em graus.
        @param angle: Ângulo de rotação em graus.
        """

        self.window.apply_rotation(angle)
