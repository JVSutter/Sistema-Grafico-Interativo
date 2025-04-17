from model.world_objects.world_object import WorldObject
from view.graphical_objects.graphical_curve import GraphicalCurve
import numpy as np
import time


class WorldCurve(WorldObject):
    """Classe pertinente a curvas de Bézier cúbicas no mundo."""
    
    def update_normalized_points(self, norm_control_points: list[tuple[float, float]]):
        """
        Atualiza as coordenadas normalizadas (NCS) dos PONTOS DE CONTROLE do objeto
        e recalcula os pontos da curva para o viewport.
        @param norm_control_points: Lista de pontos de controle normalizados.
        """

        self.normalized_points = norm_control_points
        
        generated_norm_points = self._generate_curve_points_normalized()
        
        self.viewport_points = self.transform_normalized_points_to_viewport(generated_norm_points)

    def _generate_curve_points_normalized(self, num_steps: int = 1000) -> list[tuple[float, float]]:
        """
        Gera pontos ao longo da curva de Bézier usando a forma matricial em coordenadas normalizadas.
        @param num_steps: Número de segmentos para aproximar a curva.
        @return: Lista de pontos (x, y) normalizados ao longo da curva.
        """
        
        # Faz o tratamento de pontos de controle para C(1)
        pts = list(self.normalized_points)
        for j in range(3, len(pts) - 3, 3):
            P2 = np.array(pts[j-1])
            P3 = np.array(pts[j])
            pts[j+1] = (P3 + (P3 - P2)).tolist()  

        # Matriz de Bezier
        M = np.array([
        [-1,  3, -3, 1],
        [ 3, -6,  3, 0],
        [-3,  3,  0, 0],
        [ 1,  0,  0, 0]
        ])

        # Gera T e TM 
        ts = np.linspace(0, 1, num_steps + 1) # vetor com todos os valores de t (de 0 a 1 com num_steps+1 pontos)
        T = np.vstack([ts**3, ts**2, ts, np.ones_like(ts)]).T # matriz de tamanho num_steps+1 por 4, onde cada linha é um vetor [t^3, t^2, t, 1]
        TM = T @ M
        
        # Gera os pontos da curva
        curve_points = []
        for i in range(0, len(pts) - 3, 3):
            P = np.array([[pts[x][0], pts[x][1]] for x in range(i, 4+i)])
            
            point_coords = TM @ P 
            curve_points.extend(tuple(point_coords))

        return curve_points

    def get_clipped_representation(self) -> GraphicalCurve | None:
        """
        Retorna a representação gráfica da curva após dividir em retas e aplicar clipping.
        """
        
        if not self.viewport_points:
            return None
            
        # Divide a curva em segmentos de reta
        clipped_points = []
        
        for i in range(len(self.viewport_points) - 1):
            # Para cada par de pontos consecutivos, cria uma "linha virtual"
            start_point = self.viewport_points[i]
            end_point = self.viewport_points[i+1]
            
            # Converte os pontos do viewport de volta para coordenadas normalizadas
            vp_width = self.viewport_bounds.x_max - self.viewport_bounds.x_min
            vp_height = self.viewport_bounds.y_max - self.viewport_bounds.y_min
            
            nx1 = 2 * (start_point[0] - self.viewport_bounds.x_min) / vp_width - 1
            ny1 = 1 - 2 * (start_point[1] - self.viewport_bounds.y_min) / vp_height
            
            nx2 = 2 * (end_point[0] - self.viewport_bounds.x_min) / vp_width - 1
            ny2 = 1 - 2 * (end_point[1] - self.viewport_bounds.y_min) / vp_height
            
            # Aplica o algoritmo de clipping de Cohen-Sutherland
            from model.world_objects.world_line import WorldLine
            
            # Cria uma linha temporária para usar seu algoritmo de clipping
            temp_line = WorldLine([(nx1, ny1), (nx2, ny2)], "temp", self.color, self.viewport_bounds)
            temp_line.normalized_points = [(nx1, ny1), (nx2, ny2)]
            
            # Aplica o clipping
            clipped_segment = temp_line.cohen_sutherland_clipping()
            
            # Se o segmento for visível, adiciona aos pontos recortados
            if clipped_segment is not None:
                # Converte de volta para coordenadas do viewport
                viewport_segment = self.transform_normalized_points_to_viewport(clipped_segment)
                
                # Adiciona apenas o primeiro ponto (exceto para o último segmento)
                if i < len(self.viewport_points) - 2:
                    clipped_points.append(viewport_segment[0])
                else:
                    # Para o último segmento, adiciona ambos os pontos
                    clipped_points.extend(viewport_segment)
        
        if not clipped_points:
            return None
            
        graphical_representation = GraphicalCurve(clipped_points, self.color)
        return graphical_representation
