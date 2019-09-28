from PyQt5.QtWidgets import QWidget, QPushButton, QGroupBox, QVBoxLayout, QHBoxLayout


# Стартовый виджет с выбором действия от пользователя
class StartingWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.main_layout = QVBoxLayout(self)

        self.main_group = QGroupBox()

        self.change_variant_button = QPushButton("Редактировать вариант")

        self.leftVbox = QVBoxLayout()
        self.leftVbox.addWidget(self.change_variant_button)

        self.create_variant_button = QPushButton("Создать вариант")
        self.rightVbox = QVBoxLayout()
        self.rightVbox.addWidget(self.create_variant_button)

        self.hbox = QHBoxLayout(self.main_group)
        self.hbox.addLayout(self.leftVbox)
        self.hbox.addLayout(self.rightVbox)

        self.look_at_variant_button = QPushButton("Посмотреть на воздушную обстановку")
        self.look_at_variant_button.setEnabled(False)

        self.main_layout.addWidget(self.main_group)
        self.main_layout.addWidget(self.look_at_variant_button)
