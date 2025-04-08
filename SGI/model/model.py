import os

import numpy as np

from model.window import Window
from model.world_object import WorldObject
from utils.obj_handler import ObjHandler
from view.view import View
from view.graphical_objects.point import Point
from view.graphical_objects.line import Line
from view.graphical_objects.wireframe import Wireframe

class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view: View):
        self.view = view
        self.window = Window(viewport_bounds=view.viewport.viewport_bounds)
        self.display_file = []

    @staticmethod
    def update_interface(func: callable) -> callable:
        """Decorator para atualizar a interface quando uma função é chamada."""

        def wrapper(*args, **kwargs):
            self = args[0]
            result = func(*args, **kwargs)

            # Recalcula as coordenadas normalizadas para todos os objetos
            self._calculate_and_update_scn()

            # Atualiza a View
            self.view.update_view_objects(self.display_file)

            return result

        return wrapper

    @update_interface
    def add_object(self, points: list, name: str, color: tuple) -> None:
        """Adiciona um objeto gráfico ao display file e atualiza a View."""
        
        # Confere se ja nao existe um objeto com os mesmos pontos
        if any(points == [(x, y) for x, y, *_ in objs.world_points] for objs in self.display_file):
            self.view.add_log(f"Object {name} already exists, skipping...")
            return
        
        if len(points) == 1:
            graphical_representation = Point(color)
        elif len(points) == 2:
            graphical_representation = Line(color)
        else:
            graphical_representation = Wireframe(color)
            
        tipo = graphical_representation.__class__.__name__
        
        if not name:
            name = f"{tipo} {len([obj for obj in self.display_file if obj.graphical_representation.__class__.__name__ == tipo]) + 1}"

        viewport_bounds = self.view.viewport.viewport_bounds
        world_object = WorldObject(points, name, viewport_bounds, graphical_representation)

        self.display_file.append(world_object)
        self.view.add_log(f"{tipo} {name} created: {points}")

    @update_interface
    def remove_object(self, index: int) -> None:
        """Remove um objeto do display file e atualiza a View."""

        self.display_file.pop(index)

    @update_interface
    def zoom(self, factor: float) -> None:
        """Aplica um zoom na janela de visualização e atualiza a View."""

        self.window.apply_zoom(factor)

    @update_interface
    def pan(self, dx: float, dy: float) -> None:
        """Aplica um pan na janela de visualização e atualiza a View."""

        # Rotaciona dx e dy pelo ângulo atual da window
        dx_world = dx * np.cos(self.window.angle) - dy * np.sin(self.window.angle)
        dy_world = dx * np.sin(self.window.angle) + dy * np.cos(self.window.angle)

        self.window.apply_pan(dx_world, dy_world)

    @update_interface
    def translate_object(self, index: int, dx: float, dy: float) -> None:
        """Translada um objeto no display file e atualiza a View."""

        world_object = self.display_file[index]
        translation_matrix = np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        world_object.update_coordinates([translation_matrix])

        self.view.add_log(f"{world_object.name} translated by ({dx}, {dy})")

    @update_interface
    def scale_object(self, index: int, x_factor: float, y_factor: float) -> None:
        """Escala um objeto no display file e atualiza a View."""

        world_object = self.display_file[index]
        center_x, center_y = world_object.get_center()

        translation_matrix = np.array([[1, 0, 0], [0, 1, 0], [-center_x, -center_y, 1]])
        scaling_matrix = np.array([[x_factor, 0, 0], [0, y_factor, 0], [0, 0, 1]])
        inverse_translation_matrix = np.array(
            [[1, 0, 0], [0, 1, 0], [center_x, center_y, 1]]
        )

        world_object.update_coordinates(
            [translation_matrix, scaling_matrix, inverse_translation_matrix]
        )

        self.view.add_log(f"{world_object.name} scaled by ({x_factor}, {y_factor})")

    @update_interface
    def rotate_object(self, index: int, x: float, y: float, angle: float) -> None:
        """
        Rotaciona um objeto em torno de (x, y) e atualiza a View.
        """

        angle_degrees = angle
        angle_radians = np.radians(angle)

        world_object = self.display_file[index]
        translation_matrix = np.array([[1, 0, 0], [0, 1, 0], [-x, -y, 1]])
        rotation_matrix = np.array(
            [
                [np.cos(angle_radians), np.sin(angle_radians), 0],
                [-np.sin(angle_radians), np.cos(angle_radians), 0],
                [0, 0, 1],
            ]
        )
        inverse_translation_matrix = np.array([[1, 0, 0], [0, 1, 0], [x, y, 1]])

        world_object.update_coordinates(
            [translation_matrix, rotation_matrix, inverse_translation_matrix]
        )

        self.view.add_log(
            f"{world_object.name} rotated about ({x}, {y}) by an angle of {angle_degrees}°"
        )

    @update_interface
    def rotate_window(self, angle: float) -> None:
        """Rotaciona a janela de visualização para o ângulo especificado em graus."""

        angle_radians = np.radians(angle)

        self.window.apply_rotation(angle_radians)

    def _calculate_and_update_scn(self):
        """Calcula as coordenadas normalizadas para todos os objetos e atualiza a View."""

        # 0. Obtem os parametros da window
        wcx, wcy = self.window.get_center()  # centro da window
        win_width, win_height = (
            self.window.get_width_height()
        )  # largura e altura da window

        # 1. Translada Wc para origem
        translate_to_origin = np.array([[1, 0, 0], [0, 1, 0], [-wcx, -wcy, 1]])
        transformations = translate_to_origin

        # 2. Determina vup e o angulo entre ele e o eixo y
        vup = self.window.vup
        angle_vup_y = np.arctan2(vup[1], vup[0]) - np.pi / 2
        rotation_angle_rad = -angle_vup_y

        # 3. Rotaciona o mundo para alinhar vup com o eixo y
        cos_r = np.cos(rotation_angle_rad)
        sin_r = np.sin(rotation_angle_rad)
        rotate_align_y = np.array([[cos_r, sin_r, 0], [-sin_r, cos_r, 0], [0, 0, 1]])
        transformations = transformations @ rotate_align_y

        # 4. Normaliza as coordenadas, realizando um escalonamento
        scale_x = 2.0 / win_width if win_width != 0 else 1.0
        scale_y = 2.0 / win_height if win_height != 0 else 1.0
        scale_to_scn = np.array([[scale_x, 0, 0], [0, scale_y, 0], [0, 0, 1]])
        transformations = transformations @ scale_to_scn

        # 5. Calcula a SCN e armazena no display file de cada objeto
        for obj in self.display_file:
            normalized_coords = []

            for point_wc in obj.world_points:
                point_scn = point_wc @ transformations  # Transforma o ponto WC para SCN

                nx = point_scn[0]
                ny = point_scn[1]

                normalized_coords.append((nx, ny))

            obj.update_normalized_points(normalized_coords)

    def import_obj_file(self, filepath: str) -> None:
        """Importa um arquivo .obj e adiciona os objetos ao display file."""

        obj_handler = ObjHandler()
        objects_list = obj_handler.read_obj_file(filepath)

        for obj in objects_list:

            if obj[1] in [
                [(x, y) for x, y, *_ in objs.world_points] for objs in self.display_file
            ]:
                self.view.add_log(f"Object {obj[0]} already exists, skipping...")
                continue

            self.add_object(points=obj[1], name=obj[0], color=(0, 0, 0))

        self.view.add_log(f"Objects successfully imported from {filepath}")

    def export_obj_file(self, filepath: str, name: str) -> None:
        """Exporta os objetos do display file para um arquivo .obj."""

        if not name:
            name = "output"

        filepath = os.path.join(filepath, f"{name}.obj")

        obj_handler = ObjHandler()
        obj_str = obj_handler.generate_obj_str(self.display_file)

        with open(filepath, "w") as f:
            f.write(obj_str)

        self.view.add_log(f"Objects successfully exported to {filepath}")
