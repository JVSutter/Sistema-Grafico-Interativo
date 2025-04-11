import numpy as np

from model.graphical_algorithms import GraphicalAlgorithms
from model.world_objects.world_object import WorldObject
from model.world_objects.world_object_factory import WorldObjectFactory
from utils.bounds import Bounds
from view.graphical_objects.graphical_object import GraphicalObject


class DisplayFileManager:
    """
    Classe responsável por gerenciar o display file
    """

    def __init__(self, viewport_bounds: Bounds):
        self.display_file: list[WorldObject] = []
        WorldObjectFactory.viewport_bounds = viewport_bounds

    def get_clipped_representations(self) -> list[GraphicalObject]:
        """
        Retorna as representações gráficas a serem enviadas para o viewport desenhar.
        @return: Lista de representações gráficas após o clipping.
        """

        representations = []
        for obj in self.display_file:
            representations.extend(obj.get_clipped_representation())

        return representations

    def add_object(self, points: list, name: str, color: tuple) -> bool:
        """Adiciona um objeto gráfico ao display file e atualiza a View."""

        world_object = WorldObjectFactory.new_world_object(
            points=points, name=name, color=color, display_file=self.display_file
        )

        if world_object is None:
            return False
        self.display_file.append(world_object)
        return True

    def remove_object(self, index: int) -> None:
        """Remove um objeto gráfico do display file."""
        self.display_file.pop(index)

    def convert_display_file_to_obj(self) -> str:
        """Retorna uma string com o conteúdo do display file em formato OBJ."""

        obj_str = ""
        for obj in self.display_file:
            obj_str += obj.get_obj_description()
        return obj_str

    def get_objs_as_strings(self) -> str:
        return [str(obj) for obj in self.display_file]

    def apply_transformation(
        self, index: int, transformations_list: list[dict]
    ) -> None:
        """
        Aplica uma transformação matricial a todos os objetos do display file.
        @param transformations_list: Lista de dicionários, cada um representando uma transformação.
        """

        obj = self.display_file[index]
        transformation_mtx = GraphicalAlgorithms.get_transformation_matrix(
            transformations_list=transformations_list, obj_center=obj_center
        )

        if not transformation_mtx:
            return
        obj.update_coordinates(transformation_mtx)

    def update_ncs_coordinates(
        self,
        window_cx: float,
        window_cy: float,
        window_height: float,
        window_width: float,
        window_vup: np.ndarray,
    ) -> None:
        """
        Atualiza as coordenadas do display file para o sistema de coordenadas da janela.
        @param window_cx: Coordenada x do centro da janela.
        @param window_cy: Coordenada y do centro da janela.
        @param window_vup: Vetor de direção para cima da janela.
        """

        ncs_conversion_mtx = GraphicalAlgorithms.get_ncs_transformation_matrix(
            window_cx=window_cx,
            window_cy=window_cy,
            window_vup=window_vup,
            window_height=window_height,
            window_width=window_width,
        )

        for obj in self.display_file:
            normalized_coords = []

            for point_wc in obj.world_points:
                point_ncs = (
                    point_wc @ ncs_conversion_mtx
                )  # Transforma o ponto WC para ncs

                nx = point_ncs[0]
                ny = point_ncs[1]

                normalized_coords.append((nx, ny))

            obj.update_normalized_points(normalized_coords)

    def import_file_to_display_file(self, filepath: str) -> None:
        """
        Importa um arquivo .obj e adiciona os objetos ao display file.
        @param filepath: Caminho do arquivo .obj a ser importado.
        """

        world_objects, skipped_objects = WorldObjectFactory.new_objects_from_file(
            filepath=filepath, display_file=self.display_file
        )

        for world_object in world_objects:
            self.display_file.append(world_object)

        return world_objects, skipped_objects
