import logging
from PyQt6 import QtWidgets, QtGui, QtCore
from view.bounds import Bounds

class ViewportDisplay(QtWidgets.QWidget):
    """Classe responsável por exibir os objetos gráficos no viewport."""
    
    def __init__(self, parent):
        super(ViewportDisplay, self).__init__(parent)
        self.objects = []
        
        # Define a cor de fundo do viewport
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(100, 0, 0, 100))
        self.setPalette(palette)
        
    def update_objects(self, objects, window_bounds):
        """Atualiza a lista de objetos e as dimensões da window."""
        self.objects = objects
        self.window_bounds = window_bounds
        self.update()  # Força a redesenhar a tela
        
    def resizeEvent(self, event):
        """Atualiza as dimensões do viewport quando ele é redimensionado."""
        super(ViewportDisplay, self).resizeEvent(event)
        self.viewport_bounds = Bounds(
            x_min=0,
            y_min=0,
            x_max=self.width(),
            y_max=self.height()
        )
        
    def paintEvent(self, event):
        """Desenha os objetos no viewport."""
        if not self.objects or not self.window_bounds or not self.viewport_bounds:
            return
            
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        # Define a cor e espessura da caneta
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        pen.setWidth(2)
        painter.setPen(pen)
        
        # Desenha cada objeto
        for obj in self.objects:
            self.draw_object(painter, obj)
            
    def draw_object(self, painter, obj):
        """Desenha um objeto específico no viewport."""
        transformed_points = obj.transform_points_to_viewport(
            self.viewport_bounds, self.window_bounds
        )
        
        if obj.type == "Point":
            # Desenha um ponto (círculo pequeno)
            point = transformed_points[0]
            painter.drawEllipse(QtCore.QPointF(point[0], point[1]), 3, 3)
            
        elif obj.type == "Line":
            # Desenha uma linha
            p1, p2 = transformed_points
            painter.drawLine(
                QtCore.QPointF(p1[0], p1[1]),
                QtCore.QPointF(p2[0], p2[1])
            )
            
        elif obj.type == "Wireframe":
            # Desenha um polígono
            path = QtGui.QPainterPath()
            
            # Move para o primeiro ponto
            path.moveTo(QtCore.QPointF(transformed_points[0][0], transformed_points[0][1]))
            
            # Adiciona linhas para os pontos restantes
            for point in transformed_points[1:]:
                path.lineTo(QtCore.QPointF(point[0], point[1]))
                
            # Fecha o polígono
            path.lineTo(QtCore.QPointF(transformed_points[0][0], transformed_points[0][1]))
            
            # Desenha o caminho
            painter.drawPath(path)
