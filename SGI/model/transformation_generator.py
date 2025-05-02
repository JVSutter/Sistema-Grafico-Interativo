import numpy as np


class TransformationGenerator:
    """
    Classe responsável por gerar matrizes de transformação.
    """

    @classmethod
    def _get_translation_matrix(cls, dx: float, dy: float) -> np.ndarray:
        """
        Obtém a matriz de translação.
        @param dx: Deslocamento em x.
        @param dy: Deslocamento em y.
        @return: Matriz de translação.
        """

        return np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

    @classmethod
    def _get_scaling_matrix(
        cls, sx: float, sy: float, cx: float, cy: float
    ) -> np.ndarray:
        """
        Obtém a matriz de escalonamento.
        @param sx: Fator de escalonamento em x.
        @param sy: Fator de escalonamento em y.
        @param cx: Coordenada x do centro de escalonamento.
        @param cy: Coordenada y do centro de escalonamento.
        @return: Matriz de escalonamento.
        """

        translate_to_origin = cls._get_translation_matrix(-cx, -cy)
        scale = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        translate_back = cls._get_translation_matrix(cx, cy)
        return translate_to_origin @ scale @ translate_back

    @classmethod
    def _get_rotation_matrix(
        cls, angle_degrees: float, cx: float, cy: float
    ) -> np.ndarray:
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

        translate_to_origin = cls._get_translation_matrix(-cx, -cy)
        rotate = np.array([[cos_r, sin_r, 0], [-sin_r, cos_r, 0], [0, 0, 1]])
        translate_back = cls._get_translation_matrix(cx, cy)
        return translate_to_origin @ rotate @ translate_back

    @classmethod
    def get_transformation_matrix(
        cls, transformations_list: list[dict], obj_center: tuple[float, float]
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
                matrix = cls._get_translation_matrix(dx, dy)

            elif transformation_type == "scaling":
                sx = transformation["sx"]
                sy = transformation["sy"]
                center_x, center_y = obj_center
                center_transformed = (
                    np.array([center_x, center_y, 1]) @ composite_matrix
                )
                cx_current, cy_current = center_transformed[0], center_transformed[1]
                matrix = cls._get_scaling_matrix(sx, sy, cx_current, cy_current)

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
                    matrix = cls._get_rotation_matrix(angle, cx_current, cy_current)
                else:  # origem ou ponto arbitrario
                    matrix = cls._get_rotation_matrix(angle, float(cx), float(cy))

            composite_matrix = composite_matrix @ matrix

        return composite_matrix

    @classmethod
    def _get_ncs_transformation_matrix(
        cls,
        window_cx: float,
        window_cy: float,
        window_height: float,
        window_width: float,
        window_vup: np.ndarray,
    ) -> np.ndarray:
        """
        Retorna a matriz de transformação para coordenadas normalizadas.
        @param window_cx: Coordenada x do centro da janela.
        @param window_cy: Coordenada y do centro da janela.
        @param window_vup: Vetor Vup da janela (indicando a direção "para cima").
        @return: Matriz de transformação para coordenadas normalizadas.
        """

        # 1. Translada Wc para origem
        translate_to_origin = np.array(
            [[1, 0, 0], [0, 1, 0], [-window_cx, -window_cy, 1]]
        )
        transformations = translate_to_origin

        # 2. Determina vup e o angulo entre ele e o eixo y
        angle_vup_y = np.arctan2(window_vup[1], window_vup[0]) - np.pi / 2
        rotation_angle_rad = -angle_vup_y

        # 3. Rotaciona o mundo para alinhar vup com o eixo y
        cos_r = np.cos(rotation_angle_rad)
        sin_r = np.sin(rotation_angle_rad)
        rotate_align_y = np.array([[cos_r, sin_r, 0], [-sin_r, cos_r, 0], [0, 0, 1]])
        transformations = transformations @ rotate_align_y

        # 4. Normaliza as coordenadas, realizando um escalonamento
        scale_x = 2.0 / window_width if window_width != 0 else 1.0
        scale_y = 2.0 / window_height if window_height != 0 else 1.0
        scale_to_ncs = np.array([[scale_x, 0, 0], [0, scale_y, 0], [0, 0, 1]])
        transformations = transformations @ scale_to_ncs

        return transformations

    @classmethod
    def get_parallel_projection_matrix(
        cls,
        window_center: np.ndarray,
        view_plane_normal: np.ndarray,
        window_vup: np.ndarray,
        window_width: float,
        window_height: float,
    ):
        """
        Retorna a matriz de projeção paralela.
        @param window_center: Ponto de referência da visão (centro da janela).
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

        # Passo 2: Rotacionar o mundo em torno de X e de Y de forma a alinha VPN com o eixo Z
        angle_vup_y = np.arctan2(vpn_x, vpn_z)
        rotate_y = np.array(
            [
                [np.cos(angle_vup_y), 0, np.sin(angle_vup_y), 0],
                [0, 1, 0, 0],
                [-np.sin(angle_vup_y), 0, np.cos(angle_vup_y), 0],
                [0, 0, 0, 1],
            ]
        )

        angle_vup_x = np.arctan2(vpn_y, vpn_z)
        rotate_x = np.array(
            [
                [1, 0, 0, 0],
                [0, np.cos(angle_vup_x), -np.sin(angle_vup_x), 0],
                [0, np.sin(angle_vup_x), np.cos(angle_vup_x), 0],
                [0, 0, 0, 1],
            ]
        )

        # Passo 3: Ignorar a coordenada z
        ignore_z = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1],
            ]
        )

        # Passo 4: Determinar ângulo entre o vetor Vup e o eixo Y
        angle_vup_y = np.arctan2(window_vup_y, window_vup_x) - np.pi / 2

        # Passo 5: Rotacionar o mundo para alinhar Vup com o eixo Y
        cos_r = np.cos(angle_vup_y)
        sin_r = np.sin(angle_vup_y)
        rotate_align_y = np.array(
            [
                [cos_r, sin_r, 0, 0],
                [-sin_r, cos_r, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        # Passo 6: Normalizar as coordenadas, realizando um escalonamento
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
            @ rotate_align_y
            @ scale_to_ncs
        )
        return transformation
