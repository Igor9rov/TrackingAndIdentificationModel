from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QProgressBar, QLabel


class ProgressGroupBox(QGroupBox):
    """
    GroupBox для отображения состояния моделирования
    """
    def __init__(self, parent=None):
        QGroupBox.__init__(self, title="Выполнение", parent=parent)

        # Все компоненты
        # TODO: Добавить коэффициент отношения реального времени к моделированному времени,
        #  предполагаемое время выполнения
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignHCenter)
        self.label = QLabel("Здесь будет информация о загрузке")
        self.label.setAlignment(Qt.AlignHCenter)

        # Основной контейнер
        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.label)
