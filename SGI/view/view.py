import sys
from PyQt6 import QtWidgets, uic
from view.dialogs import ObjectDialog, PointDialog, LineDialog, WireframeDialog


class View(QtWidgets.QMainWindow):
    """Classe responsavel por gerenciar a interface grafica da aplicacao"""

    def __init__(self, controller):
        self.app = QtWidgets.QApplication(sys.argv)  # Necessário estar no começo

        super().__init__()
        uic.loadUi("view/screens/main.ui", self)
        self.controller = controller

        self.define_values()
        self.connect_buttons()
        self.show()

    def define_values(self):
        """Define os valores iniciais dos widgets"""
        self.zoomSlider.setValue(50)

    def connect_buttons(self):
        """Conecta os botões da interface com os métodos correspondentes"""

        # Botões de alteração da lista de objetos
        self.createPoint.clicked.connect(lambda: self.create_object(PointDialog(), "Point"))
        self.createLine.clicked.connect(lambda: self.create_object(LineDialog(), "Line"))
        self.createWireframe.clicked.connect(lambda: self.create_object(WireframeDialog(), "Wireframe"))
        self.removeObject.clicked.connect(self.remove_object)

        # Botões de zoom
        self.zoomInButton.clicked.connect(lambda: self.zoom(self.zoomSlider.value() + 10))  # Quando aperta o botao de zoom in
        self.zoomOutButton.clicked.connect(lambda: self.zoom(self.zoomSlider.value() - 10))
        self.zoomSlider.valueChanged.connect(lambda: self.zoom(self.zoomSlider.value()))  # Quando altera o valor do zoom pela barra

        # Botões de navegação
        self.navUpButton.clicked.connect(lambda: self.pan("up"))
        self.navDownButton.clicked.connect(lambda: self.pan("down"))
        self.navLeftButton.clicked.connect(lambda: self.pan("left"))
        self.navRightButton.clicked.connect(lambda: self.pan("right"))

    def run(self):
        """Executa a aplicação PyQt"""
        sys.exit(self.app.exec())

    def add_object(self, points, name):
        """Adiciona um objeto à lista de objetos da aplicação"""

        self.controller.handle_point_input(points, name)
        self.update_object_list()  # Adiciona o objeto a lista visual

    def update_object_list(self):
        """Atualiza a lista de objetos da aplicacao"""

        object_list = self.controller.get_objects()
        self.objectsList.clear()
        self.objectsList.addItems(object_list)

    def add_log(self, message):
        """Adiciona uma mensagem ao log da aplicacao"""

        logbox = self.logsBox  # Pega o objeto que contem o log
        logbox.addItem(message)  # Adiciona a mensagem ao log
        logbox.scrollToBottom()  # Faz o log rolar para baixo para mostrar a mensagem mais recente

    def create_object(self, dialog: ObjectDialog, object_type: str):
        """Cria um objeto usando uma caixa de diálogo"""

        points, name = dialog.create_object()
        if name is not None:
            self.add_object(points, name)
            self.add_log(f"{object_type} {name} created: {points}")

    def remove_object(self):
        """Remove um objeto da lista de objetos"""

        # pega o index do item selecionado
        selected = self.objectsList.currentRow()

        # se nao tiver selecionado nenhum item
        if selected == -1:
            self.add_log("You must select an object to remove")
            return

        text = self.objectsList.currentItem().text()

        self.controller.remove_object(index=selected)
        self.update_object_list()
        self.add_log(f"{text} has been removed")

    def zoom(self, value):  # COLOCAR DEPOIS A FUNCAO DE ZOOM DO CONTROLLER AQUI
        """Altera o zoom da window"""

        self.zoomSlider.setValue(value)  # Atualiza o valor do slider
        self.add_log(f"Zoomed: {value}")

    def pan(self, direction):
        """Move a camera da window"""

        self.add_log(f"Panned {direction}")
