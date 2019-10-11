from PyQt5.QtWidgets import QMessageBox, QStyle


# Сообщение о ошибке
class ErrorMessageBox(QMessageBox):
    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent)
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Ошибка")
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxCritical))
