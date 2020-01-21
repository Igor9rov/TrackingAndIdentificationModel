from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout


class StartingWidget(QWidget):
    """Стартовый виджет с выбором действия от пользователя"""
    def __init__(self, parent=None) -> None:
        QWidget.__init__(self, parent)

        # Основные компоненты
        self.change_variant_button = QPushButton("Редактировать вариант")
        self.create_variant_button = QPushButton("Создать вариант")
        self.look_at_variant_button = QPushButton("Посмотреть на воздушную обстановку")

        # Вертикальный контенер для копок создать/редактировать вариант
        create_or_edit_layout = QHBoxLayout()
        create_or_edit_layout.addWidget(self.change_variant_button)
        create_or_edit_layout.addWidget(self.create_variant_button)

        # Основной контейнер
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(create_or_edit_layout)
        main_layout.addWidget(self.look_at_variant_button)

        self.look_at_variant_button.setEnabled(False)
