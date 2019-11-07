from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow

from start_simulation_ui import StartSimulationUI


class CreateAndEditVariantMainWindow(QMainWindow):
    """Основное окно приложения GUI для запуска моделирования"""
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # Центральный виджет
        self.setCentralWidget(StartSimulationUI())
        # Название
        self.setWindowTitle("Запуск варианта моделирования")
        # Фиксированные размеры
        self.setFixedSize(QSize(360, 300))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = CreateAndEditVariantMainWindow()
    application.show()
    sys.exit(app.exec())
