"""
Módulo com as classes relativas às caixas de diálogo para criação de objetos
"""

from PyQt6 import QtWidgets, uic


class ObjectDialog(QtWidgets.QDialog):
    """Classe responsável por gerenciar o popup de criação de objeto"""

    def __init__(self):
        super().__init__()
        uic.loadUi("view/screens/newObject.ui", self)

        self.points: list = []
        self.color: tuple = (0, 0, 0)  # Cor padrão preto
        self.name: str | None = None
        self.fill_state: bool = False  # Estado inicial do preenchimento

        self.newPointButton.clicked.connect(self.add_point)
        self.removeButton.clicked.connect(self.remove_selected_point)
        self.colorButton.clicked.connect(self.choose_color)

    def create_object(self):
        """Cria um objeto"""

        self.show()
        result = self.exec()

        # Se o usuário cancelou, retorna None para todos os valores
        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return None, None, None, None

        self.name = self.nameInput.text() if self.nameInput.text().strip() else None
        is_filled = (
            self.fillCheckBox.isChecked() if self.fillCheckBox.isEnabled() else False
        )

        return self.points, self.name, self.color, is_filled

    def add_point(self):
        """Adiciona um novo ponto à lista"""

        x = float(self.xInput.value())
        y = float(self.yInput.value())
        point = (x, y)

        self.points.append(point)
        self.pointsList.addItem(f"Point: {point}")
        self._update_interface()

    def remove_selected_point(self):
        """Remove o ponto selecionado da lista"""

        current_item = self.pointsList.currentItem()
        if current_item:
            index = self.pointsList.row(current_item)
            self.points.pop(index)
            self.pointsList.takeItem(index)
            self._update_interface()
        else:
            self.show_error_message("You must select a point to remove.")

    def choose_color(self):
        """Abre o diálogo de escolha de cor"""

        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.color = (color.red(), color.green(), color.blue())
            self.colorPreview.setStyleSheet(
                f"border: 2px solid white; border-radius: 16px; background-color: rgb{self.color};"
            )

        self.raise_()

    def show_error_message(self, message: str):
        """Mostra uma mensagem de erro"""

        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Erro")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        error_dialog.exec()

    def accept(self):
        """Sobrescreve o método accept para validar o número de pontos"""

        if len(self.points) < 1:
            self.show_error_message(
                "There must be at least 1 point to create an object."
            )
        elif self.curveRadio.isChecked() and (len(self.points)-1) % 3 != 0:
            self.show_error_message(
                """The number of points must be 4 plus a multiple of 3 for a curve.
                Example: 4, 7, 10, 13, etc.
                """
            )
        else:
            super().accept()

    def _update_fill_checkbox_visibility(self):
        """Atualiza a habilitação do checkbox 'Filled' baseado no número de pontos.
        O filled só é habilitado se o número de pontos for maior ou igual a 3 (Wireframe).
        """

        num_points = len(self.points)
        if num_points >= 3:
            self.fillCheckBox.setEnabled(True)
            self.fillCheckBox.setChecked(self.fill_state)  # Restaura o estado salvo

        else:
            self.fill_state = self.fillCheckBox.isChecked()  # Salva o estado atual
            self.fillCheckBox.setChecked(False)
            self.fillCheckBox.setEnabled(False)
    
    def _update_object_type(self):
        """Atualiza o tipo de objeto baseado no número de pontos"""

        num_points = len(self.points)
        
        if num_points == 0: # desabilita ponto
            self.pointRadio.setChecked(False)
            self.pointRadio.setEnabled(False)

        if num_points == 1: # habilita ponto
            self.pointRadio.setChecked(True)
            self.pointRadio.setEnabled(True)
            self.lineRadio.setEnabled(False)
        
        if num_points == 2: # habilita linha
            self.lineRadio.setChecked(True)
            self.lineRadio.setEnabled(True)
            self.pointRadio.setEnabled(False)
            self.wireframeRadio.setEnabled(False)

        if num_points == 3: # habilita wireframe
            self.wireframeRadio.setChecked(True)
            self.wireframeRadio.setEnabled(True)
            self.lineRadio.setEnabled(False)
            self.pointRadio.setEnabled(False)
            self.curveRadio.setEnabled(False)
            self.curveRadio.setChecked(False)

        if num_points > 3: # habilita curva
            self.curveRadio.setEnabled(True)
            
    def _update_points_number(self):
        """Atualiza o número de pontos"""

        num_points = len(self.points)
        self.numPoints.setText(f'<html><head/><body><p><span style=" font-weight:700;">Number of points:</span> {num_points}</p></body></html>')

    def _update_interface(self):
        """Atualiza a interface baseado no tipo de objeto selecionado"""

        self._update_fill_checkbox_visibility()
        self._update_object_type()
        self._update_points_number()