from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication


class PSRStartingScreen(QWidget):
    """
    Стартовый виджет с ожиданием ввода файла БД и выбора обработки результатов моделирования
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Нужные кнопки
        self.save_file_button = QPushButton(text="Выберите файл с результатами моделирования")
        self.processing_mfr_algorithms_button = QPushButton(text="Результаты работы \nалгоритмов МФР")
        self.processing_cp_algorithms_button = QPushButton(text="Результаты работы \nалгоритмов ПБУ")

        # Контейнер для конпок с выбором результатов алгоритмов
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.processing_mfr_algorithms_button)
        horizontal_layout.addWidget(self.processing_cp_algorithms_button)

        # Основной контейнер
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.save_file_button)
        main_layout.addLayout(horizontal_layout)

        self.processing_cp_algorithms_button.setEnabled(False)
        self.processing_mfr_algorithms_button.setEnabled(False)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = PSRStartingScreen()
    application.show()
    sys.exit(app.exec())
