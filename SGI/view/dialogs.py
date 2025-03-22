from abc import abstractmethod
from PyQt6 import QtWidgets, uic 
    
class ObjectDialog(QtWidgets.QDialog):
    """Classe responsavel por gerenciar um popup generico"""
    
    def __init__(self, name: str):
        super(ObjectDialog, self).__init__()
        uic.loadUi(f"view/screens/{name}.ui", self)
        
    def create_object(self, ask_for_name: bool = True):
        """Cria um objeto"""
        
        # Mostra a janela de criacao de objeto
        self.show()
            
        # Executa a janela
        result = self.exec()
        
        # Se o usuário cancelou, retorna None
        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return None, None
            
        # Pega o(s) ponto(s) 
        self.points = self.get_points()
        
        # Pega o nome do objeto
        if ask_for_name:
            self.name = NameDialog().name
        else:
            self.name = None
        
        return self.points, self.name
    
    @abstractmethod
    def get_points(self):
        pass
        
class PointDialog(ObjectDialog):
    """Classe responsavel por gerenciar o popup de criacao de um ponto"""
    
    def __init__(self):
        super(PointDialog, self).__init__("newPoint")
        
    def get_points(self):
        """Retorna as coordenadas do ponto inseridas pelo usuario"""
        
        x = float(self.xInput.text().replace(",", "."))
        y = float(self.yInput.text().replace(",", "."))
        return [(x, y)]
    
class LineDialog(ObjectDialog):
    """Classe responsavel por gerenciar o popup de criacao de uma linha"""
    
    def __init__(self):
        super(LineDialog, self).__init__("newLine")
        
    def get_points(self):
        """Retorna as coordenadas da linha inseridas pelo usuario"""
        
        x1 = float(self.x1Input.text().replace(",", "."))
        y1 = float(self.y1Input.text().replace(",", "."))
        x2 = float(self.x2Input.text().replace(",", "."))
        y2 = float(self.y2Input.text().replace(",", "."))
        return [(x1, y1), (x2, y2)]
    
class WireframeDialog(ObjectDialog):
    """Classe responsavel por gerenciar o popup de criacao de um poligono"""
    
    def __init__(self):
        super(WireframeDialog, self).__init__("newWireframe")
        
        self.points = []
        self.newPointButton.clicked.connect(self.add_point) # Conecta o botao de adicionar um ponto
        
    def add_point(self):
        point, _ = PointDialog().create_object(ask_for_name=False) # Abre um popup para inserir as coordenadas do ponto
        self.points.append(point[0])
        self.pointsList.addItem(f"Point: {point[0]}") # Adiciona o ponto a lista de pontos
        
    def get_points(self):
        """Retorna a lista de pontos que formam o poligono"""
        return self.points
    
    def accept(self):
        """Sobrescreve o método accept para validar o número de pontos"""
        if len(self.points) < 3:
            self.show_error_message()
        else:
            super().accept()
            
    def show_error_message(self):
        """Mostra uma mensagem de erro sobre o número mínimo de pontos"""
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText("It's necessary to have at least 3 points to create a wireframe.")
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        error_dialog.exec()
        
class NameDialog(QtWidgets.QDialog):
    """Classe responsavel por gerenciar o popup de insercao de nome"""
    
    def __init__(self):
        super(NameDialog, self).__init__()
        uic.loadUi("view/screens/name.ui", self)
        
        self.show()
        self.exec()
        
    def accept(self):
        """Retorna o nome inserido pelo usuario"""
        
        self.name = self.nameInput.toPlainText()
        super().accept()
    
    def reject(self):
        """Se cancela a insercao do nome, retorna None (nao cria o objeto)"""
        
        self.name = None
        super().reject()