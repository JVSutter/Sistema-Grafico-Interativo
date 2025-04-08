import sys

from PyQt6 import QtWidgets, uic

from view.creation_dialogs import NameDialog, ObjectDialog
from view.graphical_objects.graphical_object import GraphicalObject
from view.transform_dialogs import TransformationDialog
from view.viewport import Viewport


class View(QtWidgets.QMainWindow):
    """
    Classe responsavel por gerenciar a interface grafica da aplicação.
    Métodos on_* são disparados pelo usuário ao interagir com a interface.
    """

    def __init__(self, controller):
        self.app = QtWidgets.QApplication(sys.argv)  # Necessário estar no começo

        super().__init__()
        uic.loadUi("view/screens/main.ui", self)
        self.controller = controller

        self.connect_buttons()
        self.setup_viewport()
        self.show()

    def connect_buttons(self) -> None:
        """Conecta os botões da interface com os callbacks correspondentes (on_*)."""

        # Botões de alteração da lista de objetos
        self.createObject.clicked.connect(lambda: self.on_create_object(ObjectDialog()))
        self.removeObject.clicked.connect(self.on_remove_object)
        self.transformObject.clicked.connect(self.on_transform_object)

        # Botões de zoom
        self.zoomInButton.clicked.connect(
            lambda: self.on_zoom(mode="in")
        )  # Quando aperta o botao de zoom in
        self.zoomOutButton.clicked.connect(lambda: self.on_zoom(mode="out"))
        self.zoomSlider.valueChanged.connect(
            lambda: self.on_zoom(mode="slider")
        )  # Quando altera o valor do zoom pela barra

        # Botão de rotação da janela
        self.windowRotationSlider.valueChanged.connect(
            lambda: self.on_window_rotation()
        )

        # Botões de navegação
        self.navUpButton.clicked.connect(lambda: self.on_pan(direction="up"))
        self.navDownButton.clicked.connect(lambda: self.on_pan(direction="down"))
        self.navLeftButton.clicked.connect(lambda: self.on_pan(direction="left"))
        self.navRightButton.clicked.connect(lambda: self.on_pan(direction="right"))

        # Botões de importação e exportação de arquivos
        self.importButton.clicked.connect(self.import_obj_file)
        self.exportButton.clicked.connect(self.export_obj_file)

    def setup_viewport(self) -> None:
        """Configura o viewport para exibir os objetos gráficos."""

        self.viewport = Viewport(self.frame)
        self.viewport.setup_viewport()

    def run(self) -> None:
        """Executa a aplicação PyQt."""

        sys.exit(self.app.exec())

    def update_view_objects(self, objects_list: list[GraphicalObject]) -> None:
        """Atualiza a view com a lista de objetos gráficos. Atualizando o viewport e a lista de objetos."""

        self.viewport.update_viewport(
            [obj.graphical_representation for obj in objects_list]
        )
        self.objectsList.clear()
        self.objectsList.addItems([str(obj) for obj in objects_list])

    def add_log(self, message) -> None:
        """Adiciona uma mensagem ao log da aplicação"""

        logbox = self.logsBox  # Pega o objeto que contem o log
        logbox.addItem(message)  # Adiciona a mensagem ao log
        logbox.scrollToBottom()  # Faz o log rolar para baixo para mostrar a mensagem mais recente

    def on_create_object(self, dialog: ObjectDialog) -> None:
        """Trata requisições de criação de objetos usando uma caixa de diálogo."""

        points, name, color = dialog.create_object()
        if points is not None:
            self.controller.handle_create_object(points, name, color)

    def on_remove_object(self) -> None:
        """Trata requisições de remoção de objetos no mundo."""

        selected = self.objectsList.currentRow()

        if selected == -1:
            self.add_log("You must select an object to remove")
            return

        text = self.objectsList.currentItem().text()

        self.controller.handle_remove_object(index=selected)
        self.add_log(f"{text} has been removed")

    def on_transform_object(self) -> None:
        """Trata requisições de transformação de objetos no mundo."""

        selected = self.objectsList.currentRow()

        if selected == -1:
            self.add_log("You must select an object to transform")
            return

        transformation_info = TransformationDialog().get_transformation()
        self.controller.handle_transformation(
            index=selected, transformation_info=transformation_info
        )

    def on_zoom(self, mode: str) -> None:
        """
        Trata as requisições de zoom.
        Slide no meio = 50% de zoom
        Slide no máximo = 100% de zoom (dobro do tamanho original)
        Slide no mínimo = 1% de zoom (1/100 do tamanho original)
        """

        value = 10

        if mode == "in":
            value += self.zoomSlider.value()
        elif mode == "out":
            value = self.zoomSlider.value() - value
        else:
            value = self.zoomSlider.value()

        # Evitar recursão infinita
        if self.zoomSlider.value() != value:
            self.zoomSlider.setValue(value)
            return

        # Verificar se o atributo zoom_value existe antes de usar
        if not hasattr(self, "zoom_value"):
            self.zoom_value = 50.0  # Valor inicial padrão

        old_zoom_value = self.zoom_value
        new_zoom_value = value

        # Aplica zoom apenas se houver mudança significativa
        if abs(new_zoom_value - old_zoom_value) > 0.01:
            relative_change = new_zoom_value / old_zoom_value
            self.controller.handle_zoom(
                1 / relative_change  # Pois o zoom aumenta com a diminuição da Window
            )

            self.zoomLabel.setText(f"{new_zoom_value}%")
            self.zoom_value = new_zoom_value

    def on_window_rotation(self) -> None:
        """Trata as requisições de rotação da janela."""

        self.window_rotation = self.windowRotationSlider.value()
        self.windowRotationLabel.setText(f"{self.window_rotation}º")

        self.controller.handle_window_rotation(self.window_rotation)

    def on_pan(self, direction: str) -> None:
        """Trata as requisições de pan."""

        movement = 10
        dx, dy = {
            "up": (0, movement),
            "down": (0, -movement),
            "left": (-movement, 0),
            "right": (movement, 0),
        }[direction]

        self.controller.handle_pan(dx, dy)
        self.add_log(f"Went {direction} by {dx}, {dy}")

    def import_obj_file(self) -> None:
        """Importa um arquivo .obj."""

        filepath = self.open_import_file_dialog()
        if filepath:
            self.controller.handle_import_obj_file(filepath)

    def export_obj_file(self) -> None:
        """Exporta um arquivo .obj."""

        filepath, name = self.open_export_file_dialog()
        if filepath:
            self.controller.handle_export_obj_file(filepath, name)

    def open_import_file_dialog(self) -> str:
        """Abre um diálogo para selecionar um arquivo."""

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("*.obj")

        if file_dialog.exec():
            return file_dialog.selectedFiles()[0]
        return None

    def open_export_file_dialog(self) -> tuple[str, str]:
        """Abre um diálogo para selecionar uma pasta."""
        
        display_file = self.controller.get_display_file()

        if len(display_file) == 0:
            self.add_log("You must create an object to export")
            return None, None

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)

        name_dialog = NameDialog("Give a name to the file").name

        if file_dialog.exec():
            return (file_dialog.selectedFiles()[0], name_dialog)
        return None, None
