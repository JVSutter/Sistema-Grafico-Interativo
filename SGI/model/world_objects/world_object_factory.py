from model.world_objects.world_line import WorldLine
from model.world_objects.world_point import WorldPoint
from model.world_objects.world_wireframe import WorldWireframe
from utils.bounds import Bounds


class WorldObjectFactory:
    """
    Uma classe de fábrica para instanciar objetos no mundo
    """

    viewport_bounds: Bounds = None

    @classmethod
    def new_world_object(
        cls, points: list, name: str, color: tuple, display_file: list
    ):
        """
        Cria um novo objeto do mundo a partir de uma lista de pontos.
        """

        if any(
            points == [(x, y) for x, y, *_ in objs.world_points]
            for objs in display_file
        ):
            return None

        if len(points) == 1:
            obj_type = WorldPoint
        elif len(points) == 2:
            obj_type = WorldLine
        else:
            obj_type = WorldWireframe

        if not name:
            obj_type_name = obj_type.__class__.__name__.replace("World", "")
            objects_with_same_type = [
                obj
                for obj in display_file
                if obj.__class__.__name__.replace("World", "") == obj_type_name
            ]
            name = f"{obj_type_name} {len(objects_with_same_type) + 1}"

        return obj_type(points, name, color, cls.viewport_bounds)

    @classmethod
    def read_obj_file(cls, filepath: str) -> list:
        """
        Realiza o parsing de um arquivo Wavefront OBJ, extraindo informações sobre objetos.
        """

        vertices = []  # Armazena todos os vértices (x, y) lidos
        objects_list = []  # Lista final [nome, [(x,y), ...]]
        current_object_name = "Object 0"  # Nome padrão se nenhum 'o' for encontrado
        current_object_points = []  # Pontos (x,y) do objeto atual

        try:
            with open(filepath, "r") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split()
                    command = parts[0].lower()  # tipo do comando

                    if command == "v":  # Define um vértice

                        x = float(parts[1])
                        y = float(parts[2])
                        vertices.append((x, y))

                    elif command == "o":  # Define o nome do objeto

                        if current_object_points:
                            objects_list.append(
                                [current_object_name, current_object_points]
                            )

                        current_object_name = (
                            parts[1]
                            if len(parts) > 1
                            else f"Object {len(objects_list) + 1}"
                        )
                        current_object_points = []

                    elif command in (
                        "f",
                        "l",
                        "p",
                    ):  # Define uma face ou linha ou ponto

                        indices = []
                        for part in parts[1:]:
                            try:
                                indices.append(int(part))
                            except ValueError:
                                break

                        for index in indices:
                            if index > 0:
                                vertex_index = index - 1

                            elif index < 0:
                                vertex_index = index

                            else:
                                raise ValueError(
                                    f"Índice de vértice inválido (0) na linha {line_num}"
                                )

                            current_object_points.append(vertices[vertex_index])

            # Adiciona o último objeto lido se ele tiver pontos
            if current_object_points:
                objects_list.append([current_object_name, current_object_points])

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}") from e
        except Exception as e:
            raise Exception(f"Erro ao processar o arquivo {filepath}: {e}") from e

        return objects_list

    @classmethod
    def new_objects_from_file(cls, filepath: str, display_file: list) -> list:
        """
        Lê um arquivo OBJ e cria novos objetos do mundo a partir dele.

        @param filepath: Caminho do arquivo OBJ a ser lido.
        @param display_file: Lista de objetos do mundo já existentes.
        @returns: Uma lista de objetos do mundo criados e uma lista de objetos que foram pulados
        (porque já existem no display_file).
        """

        objects_list = cls.read_obj_file(filepath)
        world_objects = []
        skipped_objects = []

        for obj_data in objects_list:
            obj_name = obj_data[0]
            obj_points = obj_data[1]

            world_object = cls.new_world_object(
                points=obj_points,
                name=obj_name,
                color=(0, 0, 0),
                display_file=display_file,
            )

            if world_object is None:
                skipped_objects.append(obj_name)
            else:
                world_objects.append(world_object)

        return world_objects, skipped_objects
