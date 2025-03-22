import sys
from PyQt6 import QtWidgets, uic
from view.dialogs import PointDialog, LineDialog, WireframeDialog
from view.viewport_display import ViewportDisplay


class View:
    """Classe responsavel por gerenciar a interface grafica da aplicacao"""
    
    def __init__(self, controller):
        self.controller = controller
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow(controller, self)
        
    def run(self):
        """Inicia a execução da interface gráfica."""
        sys.exit(self.app.exec())
        
    def update_viewport(self):
        """Atualiza o viewport com os objetos atuais."""
        self.window.update_viewport_display()
        

class MainWindow(QtWidgets.QMainWindow):
    """Classe responsavel por gerenciar a janela principal da aplicacao"""
    
    def __init__(self, controller, view):
        super(MainWindow, self).__init__()
        uic.loadUi("view/screens/main.ui", self) 
        self.controller = controller
        self.view = view
        
        # Inicializa o viewport
        self.setup_viewport()
        
        self.define_values()
        self.connect_buttons()
        self.show()
        
    def setup_viewport(self):
        """Configura o viewport para exibir os objetos gráficos."""
        self.viewport_display = ViewportDisplay(self.frame)
        
        # Adiciona o viewport ao layout do frame
        layout = QtWidgets.QVBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.viewport_display)
        self.frame.setLayout(layout)
        
    def update_viewport_display(self):
        """Atualiza o viewport com os objetos atuais e as dimensões da window."""
        # Get the actual GraphicalObject instances, not their string representations
        objects = self.controller.get_objects()
        window_bounds = self.controller.get_window_bounds()
        self.update_object_list()
        self.viewport_display.update_objects(objects, window_bounds)
        
    def define_values(self):
        """Define os valores iniciais dos widgets"""
        zoom = 50
        self.zoomSlider.setValue(zoom)
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setMaximum(100)
        
    def connect_buttons(self):
        """Conecta os botoes da interface com as funcoes correspondentes"""
        # botoes de alteracao da lista de objetos
        self.createPoint.clicked.connect(self._create_point)
        self.createLine.clicked.connect(self._create_line)
        self.createWireframe.clicked.connect(self._create_wireframe)
        self.removeObject.clicked.connect(self._remove_object)

        # botoes de zoom
        self.zoomInButton.clicked.connect(lambda: self._handle_zoom(self.zoomSlider.value() + 10))
        self.zoomOutButton.clicked.connect(lambda: self._handle_zoom(self.zoomSlider.value() - 10)) 
        self.zoomSlider.valueChanged.connect(lambda: self._handle_zoom(self.zoomSlider.value()))

        # Botoes de navegacao
        self.navUpButton.clicked.connect(lambda: self._handle_pan("up"))
        self.navDownButton.clicked.connect(lambda: self._handle_pan("down"))
        self.navLeftButton.clicked.connect(lambda: self._handle_pan("left"))
        self.navRightButton.clicked.connect(lambda: self._handle_pan("right"))
        
    def _handle_object_creation(self, points, name):
        """Trata a criação de objetos através do controller."""
        if name is not None:
            self.controller.handle_object_creation(points, name)
            self.add_log(f"{points[-1][0]} {name} created: {points}")
        
    def update_object_list(self):
        """Atualiza a lista de objetos da aplicacao."""
        # Use string representations for the list display
        object_list = self.controller.get_object_strings()
        self.objectsList.clear()
        self.objectsList.addItems(object_list)
        
    def add_log(self, message):
        """Adiciona uma mensagem ao log da aplicacao."""
        logbox = self.logsBox 
        logbox.addItem(message)
        logbox.scrollToBottom()
        
    def _handle_zoom(self, value):
        """Trata as requisições de zoom."""
        # Evitar recursão infinita
        if self.zoomSlider.value() != value:
            self.zoomSlider.setValue(value)
            return
            
        old_value = 1.0  # Valor a ser obtido do controller
        new_value = value / 50.0  # 50 no slider = fator 1.0
        
        # Aplica zoom apenas se houver mudança significativa
        if abs(new_value - old_value) > 0.01:
            zoom_factor = new_value / old_value
            self.controller.handle_zoom(zoom_factor)
            self.add_log(f"Zoomed: {value} (factor: {new_value:.2f})")
        
    def _handle_pan(self, direction):
        """Trata as requisições de panning."""
        self.controller.handle_pan(direction)
        self.add_log(f"Panned {direction}")

    def _create_point(self):
        """Cria um ponto."""
        points, name = PointDialog().create_object()
        self._handle_object_creation(points, name)

    def _create_line(self):
        """Cria uma linha."""
        points, name = LineDialog().create_object()
        self._handle_object_creation(points, name)

    def _create_wireframe(self):
        """Cria um poligono."""
        points, name = WireframeDialog().create_object()
        self._handle_object_creation(points, name)

    def _remove_object(self):
        """Remove um objeto da lista de objetos."""
        # pega o index do item selecionado
        selected = self.objectsList.currentRow()
        
        # se nao tiver selecionado nenhum item
        if selected == -1:
            self.add_log(f"You must select an object to remove")
            return
        
        text = self.objectsList.currentItem().text()
        self.controller.remove_object(index=selected)
        self.add_log(f"{text} has been removed")
