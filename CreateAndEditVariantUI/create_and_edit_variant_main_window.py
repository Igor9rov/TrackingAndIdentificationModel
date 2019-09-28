import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication

from edit_variant_stacked_widget import EditVariantStackedWidget


# Основное окно приложения
class CreateAndEditVariantMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        # Название
        self.setWindowTitle("Создание/Редактирование параметров моделирования")
        mdi_area = QtWidgets.QMdiArea()
        self.setCentralWidget(mdi_area)
        layout = QtWidgets.QVBoxLayout(mdi_area)
        # Стек виджетов
        edit_variant_widget = EditVariantStackedWidget(mdi_area)
        layout.addWidget(edit_variant_widget)
        # Фиксированные размеры
        self.setFixedSize(QtCore.QSize(600, 480))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = CreateAndEditVariantMainWindow()
    application.show()
    sys.exit(app.exec())
