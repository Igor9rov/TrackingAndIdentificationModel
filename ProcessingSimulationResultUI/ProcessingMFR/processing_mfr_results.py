from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication

from choice_mfr_number import ChoiceMFRNumber
from choice_mode import ChoiceMode
from choice_realization_number import ChoiceRealizationNumber
from choice_target_number import ChoiceTargetNumber
from mfr_result_group_box import MFRResultGroupBox


class ProcessingMFRResults(QWidget):
    """Виджет для обработки результатов работы МФР"""
    def __init__(self, parent=None) -> None:
        QWidget.__init__(self, parent)

        # Нужные виджеты
        self.choice_mode = ChoiceMode()
        self.choice_realization_number = ChoiceRealizationNumber()
        self.choice_mfr_number = ChoiceMFRNumber()
        self.choice_target_number = ChoiceTargetNumber()
        self.accept_button = QPushButton(text="Подтвердить выбор")
        self.mfr_results_group_box = MFRResultGroupBox()
        self.back_button = QPushButton(text="Назад")

        # Основной контейнер
        layout = QVBoxLayout(self)
        layout.addWidget(self.choice_mode)
        layout.addWidget(self.choice_realization_number)
        layout.addWidget(self.choice_mfr_number)
        layout.addWidget(self.choice_target_number)
        layout.addWidget(self.accept_button)
        layout.addWidget(self.mfr_results_group_box)
        layout.addWidget(self.back_button)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = ProcessingMFRResults()
    application.show()
    sys.exit(app.exec())
