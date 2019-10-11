from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication

from choice_mfr_numbers import ChoiceMFRNumbers
from choice_realization_number import ChoiceRealizationNumber
from choice_target_numbers import ChoiceTargetNumbers
from cp_result_group_box import CPResultGroupBox


class ProcessingCPResults(QWidget):
    """
    Виджет для предложения выбора трасс, просмотра результатов
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Нужные виджеты
        self.choice_realization_number = ChoiceRealizationNumber()
        self.choice_mfr_numbers = ChoiceMFRNumbers()
        self.choice_target_numbers = ChoiceTargetNumbers()
        self.accept_button = QPushButton(text="Подтвердить выбор")
        self.result_group_box = CPResultGroupBox()
        self.back_button = QPushButton(text="Назад")

        # Основной контейнер
        layout = QVBoxLayout(self)
        layout.addWidget(self.choice_realization_number)
        layout.addWidget(self.choice_mfr_numbers)
        layout.addWidget(self.choice_target_numbers)
        layout.addWidget(self.accept_button)
        layout.addWidget(self.result_group_box)
        layout.addWidget(self.back_button)

        self.result_group_box.setEnabled(False)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = ProcessingCPResults()
    application.show()
    sys.exit(app.exec())
