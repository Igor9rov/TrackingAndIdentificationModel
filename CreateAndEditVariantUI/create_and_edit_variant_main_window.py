from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow

from create_and_edit_variant_stacked_widget import EditVariantStackedWidget


class CreateAndEditVariantMainWindow(QMainWindow):
    """Основное окно приложения"""
    def __init__(self, parent=None) -> None:
        QMainWindow.__init__(self, parent)
        # Центральный виджет
        self.setCentralWidget(EditVariantStackedWidget())
        # Название
        self.setWindowTitle("Создание/Редактирование параметров моделирования")
        # Фиксированные размеры
        self.setFixedSize(QSize(660, 800))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = CreateAndEditVariantMainWindow()
    application.show()
    sys.exit(app.exec())
