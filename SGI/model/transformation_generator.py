import numpy as np


class TransformationGenerator:
    """
    Classe responsável por gerar matrizes de transformação.
    """

    @staticmethod
    def get_translation_matrix(dx: float, dy: float) -> np.ndarray:
        """
        Obtém a matriz de translação.
        @param dx: Deslocamento em x.
        @param dy: Deslocamento em y.
        @return: Matriz de translação.
        """

        return np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

    @staticmethod
    def get_scaling_matrix(sx: float, sy: float, cx: float, cy: float) -> np.ndarray:
        """
        Obtém a matriz de escalonamento.
        @param sx: Fator de escalonamento em x.
        @param sy: Fator de escalonamento em y.
        @param cx: Coordenada x do centro de escalonamento.
        @param cy: Coordenada y do centro de escalonamento.
        @return: Matriz de escalonamento.
        """

        translate_to_origin = TransformationGenerator.get_translation_matrix(-cx, -cy)
        scale = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        translate_back = TransformationGenerator.get_translation_matrix(cx, cy)
        return translate_to_origin @ scale @ translate_back

    @staticmethod
    def get_rotation_matrix(angle_degrees: float, cx: float, cy: float) -> np.ndarray:
        """
        Obtém a matriz de rotação.
        @param angle_degrees: Ângulo de rotação em graus.
        @param cx: Coordenada x do centro de rotação.
        @param cy: Coordenada y do centro de rotação.
        @return: Matriz de rotação.
        """

        angle_radians = np.radians(angle_degrees)
        cos_r = np.cos(angle_radians)
        sin_r = np.sin(angle_radians)

        translate_to_origin = TransformationGenerator.get_translation_matrix(-cx, -cy)
        rotate = np.array([[cos_r, sin_r, 0], [-sin_r, cos_r, 0], [0, 0, 1]])
        translate_back = TransformationGenerator.get_translation_matrix(cx, cy)
        return translate_to_origin @ rotate @ translate_back

    @staticmethod
    def get_transformation_matrix(
        transformations_list: list[dict], obj_center: tuple[float, float]
    ) -> np.ndarray | None:
        """
        Método para obtenção de uma matriz de transformação composta.
        @param transformations_list: Lista de dicionários, cada um representando uma transformação.
        @param obj_center: Centro do objeto a ser transformado. Usado no escalonamento e na rotação.
        @return: Matriz que produzirá uma transformação equivalente a todas as transformações individuais.
        None se a lista estiver vazia.
        """

        if not transformations_list:
            return None

        # Inicializa a matriz composta como a matriz identidade
        composite_matrix = np.identity(3)

        for transformation in transformations_list:
            transformation_type = transformation["type"]
            matrix = np.identity(3)

            if transformation_type == "translation":
                dx = transformation["dx"]
                dy = transformation["dy"]
                matrix = TransformationGenerator.get_translation_matrix(dx, dy)

            elif transformation_type == "scaling":
                sx = transformation["sx"]
                sy = transformation["sy"]
                center_x, center_y = obj_center
                center_transformed = (
                    np.array([center_x, center_y, 1]) @ composite_matrix
                )
                cx_current, cy_current = center_transformed[0], center_transformed[1]
                matrix = TransformationGenerator.get_scaling_matrix(
                    sx, sy, cx_current, cy_current
                )

            elif transformation_type == "rotation":
                angle = transformation["angle"]
                cx = transformation["cx"]
                cy = transformation["cy"]

                if cx == "obj_center":
                    center_x, center_y = obj_center
                    center_transformed = (
                        np.array([center_x, center_y, 1]) @ composite_matrix
                    )
                    cx_current, cy_current = (
                        center_transformed[0],
                        center_transformed[1],
                    )
                    matrix = TransformationGenerator.get_rotation_matrix(
                        angle, cx_current, cy_current
                    )
                else:  # origem ou ponto arbitrario
                    matrix = TransformationGenerator.get_rotation_matrix(
                        angle, float(cx), float(cy)
                    )

            composite_matrix = composite_matrix @ matrix

        return composite_matrix

    @staticmethod
    def get_x_axis_rotation_matrix(angle_degrees: float) -> np.ndarray:
        """
        Obtém a matriz de rotação em torno do eixo x.
        @return: Matriz de rotação em torno do eixo x.
        """

        angle_radians = np.radians(angle_degrees)
        cos_r = np.cos(angle_radians)
        sin_r = np.sin(angle_radians)

        return np.array(
            [
                [1, 0, 0, 0],
                [0, cos_r, -sin_r, 0],
                [0, sin_r, cos_r, 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_y_axis_rotation_matrix(angle_degrees: float) -> np.ndarray:
        """
        Obtém a matriz de rotação em torno do eixo y.
        @param angle_degrees: Ângulo de rotação em graus.
        @return: Matriz de rotação em torno do eixo y.
        """
        angle_radians = np.radians(angle_degrees)
        cos_r = np.cos(angle_radians)
        sin_r = np.sin(angle_radians)
        return np.array(
            [
                [cos_r, 0, sin_r, 0],
                [0, 1, 0, 0],
                [-sin_r, 0, cos_r, 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_z_axis_rotation_matrix(angle_degrees: float) -> np.ndarray:
        """
        Obtém a matriz de rotação em torno do eixo z.
        @param angle_degrees: Ângulo de rotação em graus.
        @return: Matriz de rotação em torno do eixo z.
        """
        angle_radians = np.radians(angle_degrees)
        cos_r = np.cos(angle_radians)
        sin_r = np.sin(angle_radians)
        return np.array(
            [
                [cos_r, -sin_r, 0, 0],
                [sin_r, cos_r, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_parallel_projection_matrix(
        window_center: np.ndarray,
        view_plane_normal: np.ndarray,
        window_vup: np.ndarray,
        window_width: float,
        window_height: float,
    ):
        """
        Retorna a matriz de projeção paralela.
        @param window_center: Centro da janela, que será usado como view reference point (VRP).
        @param view_plane_normal: Vetor normal ao plano de visão.
        @param window_vup: Vetor Vup da janela (indicando a direção "para cima").
        @param window_width: Largura da janela.
        @param window_height: Altura da janela.
        @return: Matriz de projeção paralela.
        """

        window_cx, window_cy, window_cz = window_center
        print(f"Window center: {window_center}")
        vpn_x, vpn_y, vpn_z = view_plane_normal
        window_vup_x, window_vup_y, _ = window_vup

        # Passo 1: Translação do centro da janela para a origem
        translate_vrp_to_origin = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [-window_cx, -window_cy, -window_cz, 1],
            ]
        )

        # Passo 2: Rotacionar o mundo em torno de x e de u de forma a alinhar VPN com o eixo z
        angle_vpn_xz = np.degrees(
            np.arctan2(vpn_z, vpn_x) - np.pi / 2
        )  # Ângulo que falta para colocar VPN no plano zy
        rotate_y = TransformationGenerator.get_y_axis_rotation_matrix(angle_vpn_xz)

        angle_vpn_yz = np.degrees(
            np.arctan2(vpn_z, vpn_y) - np.pi / 2
        )  # Ângulo que falta para alinhar VPN com o eixo z
        rotate_x = TransformationGenerator.get_x_axis_rotation_matrix(angle_vpn_yz)

        # Passo 3: Ignorar a coordenada z
        ignore_z = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1],
            ]
        )

        # Passo 4: Rotacionar o mundo para alinhar Vup com o eixo y
        angle_vup_y = np.degrees(np.arctan2(window_vup_y, window_vup_x) - np.pi / 2)
        align_vup_with_y = TransformationGenerator.get_z_axis_rotation_matrix(angle_vup_y)

        # Passo 5: Normalizar as coordenadas, realizando um escalonamento
        scale_x = 2.0 / window_width
        scale_y = 2.0 / window_height
        scale_to_ncs = np.array(
            [
                [scale_x, 0, 0, 0],
                [0, scale_y, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        transformation = (
            translate_vrp_to_origin
            @ rotate_y
            @ rotate_x
            @ ignore_z
            @ align_vup_with_y
            @ scale_to_ncs
        )
        return transformation
