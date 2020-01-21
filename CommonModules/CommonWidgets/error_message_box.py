from PyQt5.QtWidgets import QMessageBox, QStyle


class ErrorMessageBox(QMessageBox):
    """Сообщение о ошибке"""
    def __init__(self, parent=None) -> None:
        QMessageBox.__init__(self, parent)
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Ошибка")
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxCritical))
