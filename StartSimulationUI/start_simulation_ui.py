from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout

from choice_input_file_group_box import ChoiceInputFileGroupBox
from choise_output_file_group_box import ChoiceOutputFileGroupBox
from control_buttons_layout import ControlButtonsLayout
from generated_variant import GeneratedVariant
from progress_group_box import ProgressGroupBox
from simulation_thread import SimulationThread


class StartSimulationUI(QWidget):
    """
    GUI для запуска моделирования
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("Запуск варианта моделирования")

        # Основные компоненты
        self.choice_input_file_group_box = ChoiceInputFileGroupBox()
        self.choice_output_file_group_box = ChoiceOutputFileGroupBox()
        self.progress_group_box = ProgressGroupBox()
        self.control_buttons_layout = ControlButtonsLayout()

        # Основной контейнер
        layout = QVBoxLayout(self)
        layout.addWidget(self.choice_input_file_group_box)
        layout.addWidget(self.choice_output_file_group_box)
        layout.addWidget(self.progress_group_box)
        layout.addLayout(self.control_buttons_layout)

        self.simulation_thread = None
        # Связь кнопки для начала моделирования
        self.control_buttons_layout.start_button.clicked.connect(self.on_starting)
        # Когда сделали вариант, то активировать кнопку старт
        self.choice_input_file_group_box.variant_ready_signal.connect(self.control_buttons_layout.start_button_on)

    @pyqtSlot()
    def on_ending(self):
        """
        Слот при окончании работы потока
        :return: None
        """
        # Включение кнопок старта моделирования и выбора файлов
        self.control_buttons_layout.start_button.setEnabled(True)
        self.choice_input_file_group_box.button.setEnabled(True)
        # Показать время записи в файл
        self.progress_group_box.show_writing_time()

    @pyqtSlot()
    def on_starting(self):
        """
        Слот при нажатии кнопки старт моделирования
        :return: None
        """
        # Отключили кнопки
        self.choice_input_file_group_box.button.setEnabled(False)
        self.control_buttons_layout.start_button.setEnabled(False)
        # Укажем тип варианта, чтобы потом избежать ошибок при рефакторинге
        variant: GeneratedVariant = self.choice_input_file_group_box.variant
        # Подготовим виджеты с прогрессбаром
        self.progress_group_box.prepare_for_simulation(variant.repeating_time)
        # Создали экземпляр потока, который будет запускать пул процессов
        self.simulation_thread = SimulationThread(variant)
        # Связь с прогресс баром
        self.simulation_thread.ending_simulation.connect(self.progress_group_box.show_simulation_time)
        self.simulation_thread.finished.connect(self.on_ending)
        # Запуск потока
        self.simulation_thread.start()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = StartSimulationUI()
    application.show()
    sys.exit(app.exec())
