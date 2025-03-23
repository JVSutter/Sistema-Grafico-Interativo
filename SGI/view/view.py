import sys

from PyQt6 import QtWidgets, uic

from view.dialogs import LineDialog, ObjectDialog, PointDialog, WireframeDialog
from view.graphical_objects.graphical_object import GraphicalObject
from view.viewport import Viewport


class View(QtWidgets.QMainWindow):
    """Classe responsavel por gerenciar a interface grafica da aplicação"""

    def __init__(self, controller):
        self.app = QtWidgets.QApplication(sys.argv)  # Necessário estar no começo

        super().__init__()
        uic.loadUi("view/screens/main.ui", self)
        self.controller = controller

        self.define_values()
        self.connect_buttons()
        self.setup_viewport()
        self.show()

    def define_values(self):
        """Define os valores iniciais dos widgets"""
        self.zoom_factor = 1.0
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setMaximum(100)
        self.zoomSlider.setValue(50)

    def connect_buttons(self) -> None:
        """Conecta os botões da interface com os callbacks correspondentes (on_*)."""

        # Botões de alteração da lista de objetos
        self.createPoint.clicked.connect(lambda: self.on_create_object(PointDialog(), "Point"))
        self.createLine.clicked.connect(lambda: self.on_create_object(LineDialog(), "Line"))
        self.createWireframe.clicked.connect(lambda: self.on_create_object(WireframeDialog(), "Wireframe"))
        self.removeObject.clicked.connect(self.on_remove_object)

        # Botões de zoom
        self.zoomInButton.clicked.connect(lambda: self.on_zoom(self.zoomSlider.value() + 10))  # Quando aperta o botao de zoom in
        self.zoomOutButton.clicked.connect(lambda: self.on_zoom(self.zoomSlider.value() - 10))
        self.zoomSlider.valueChanged.connect(lambda: self.on_zoom(self.zoomSlider.value()))  # Quando altera o valor do zoom pela barra

        # Botões de navegação
        self.navUpButton.clicked.connect(lambda: self.on_pan(dx=0, dy=10))
        self.navDownButton.clicked.connect(lambda: self.on_pan(dx=0, dy=-10))
        self.navLeftButton.clicked.connect(lambda: self.on_pan(dx=-10, dy=0))
        self.navRightButton.clicked.connect(lambda: self.on_pan(dx=10, dy=0))

    def setup_viewport(self) -> None:
        """Configura o viewport para exibir os objetos gráficos."""
        self.viewport = Viewport(self.frame)

        # Adiciona o viewport ao layout do frame
        layout = QtWidgets.QVBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.viewport)
        self.frame.setLayout(layout)

    def run(self) -> None:
        """Executa a aplicação PyQt."""
        sys.exit(self.app.exec())

    def update_viewport(self, objects_list: list[GraphicalObject]) -> None:
        """
        Atualiza o viewport com a lista de objetos. Chamado pelo model quando os
        objetos são alterados.
        """
        self.viewport.update_viewport(objects_list)

    def update_object_list(self, object_list: list) -> None:
        """
        Atualiza a lista de objetos exibida na interface.
        Chamado pelo model quando a lista de objetos é alterada.
        """

        self.objectsList.clear()
        self.objectsList.addItems(object_list)

    def add_log(self, message) -> None:
        """Adiciona uma mensagem ao log da aplicação"""

        logbox = self.logsBox  # Pega o objeto que contem o log
        logbox.addItem(message)  # Adiciona a mensagem ao log
        logbox.scrollToBottom()  # Faz o log rolar para baixo para mostrar a mensagem mais recente

    def on_create_object(self, dialog: ObjectDialog, object_type: str) -> None:
        """Solicita criação de um objeto usando uma caixa de diálogo."""

        points, name = dialog.create_object()
        if name is not None:
            self.controller.handle_point_input(points, name)
            self.add_log(f"{object_type} {name} created: {points}")

    def on_remove_object(self) -> None:
        """Solicita remoção de um objeto da lista de objetos."""

        # pega o index do item selecionado
        selected = self.objectsList.currentRow()

        # se nao tiver selecionado nenhum item
        if selected == -1:
            self.add_log("You must select an object to remove")
            return

        text = self.objectsList.currentItem().text()

        self.controller.handle_remove_object(index=selected)
        self.add_log(f"{text} has been removed")

    def on_zoom(self, value):
        """Trata as requisições de zoom."""

        # Evitar recursão infinita
        if self.zoomSlider.value() != value:
            self.zoomSlider.setValue(value)
            return

        old_zoom_factor = self.zoom_factor
        new_zoom_factor = value / 50.0  # 50 no slider = fator 1.0

        # Aplica zoom apenas se houver mudança significativa
        if abs(new_zoom_factor - old_zoom_factor) > 0.01:
            relative_change = new_zoom_factor / old_zoom_factor
            self.controller.handle_zoom(1 / relative_change)  # Pois o zoom aumenta com a diminuição da Window
            self.zoom_factor = new_zoom_factor
            self.add_log(f"Zoomed: {value} (factor: {new_zoom_factor:.2f}%)")

    def on_pan(self, dx: float, dy: float) -> None:
        """Trata as requisições de pan."""

        self.controller.handle_pan(dx, dy)
        self.add_log(f"Panned by ({dx}, {dy})")
