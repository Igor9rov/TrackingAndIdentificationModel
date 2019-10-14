from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout

from choice_input_file_group_box import ChoiceInputFileGroupBox
from choise_output_file_group_box import ChoiceOutputFileGroupBox
from control_buttons_layout import ControlButtonsLayout
from progress_group_box import ProgressGroupBox
from simulation_thread import SimulationThread


class StartSimulationUI(QWidget):
    """
    GUI для запуска моделирования
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

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

        # Создаем экземпляр класса
        self.simulation_thread = SimulationThread()
        # Связь кнопки для начала моделирования
        self.control_buttons_layout.start_button.clicked.connect(self.start_simulate)
        # Связь кнопки для открытия варианта моделирования
        self.choice_input_file_group_box.button.clicked.connect(self.choice_input_file_group_box.open_existing_variant)
        # Когда сделали вариант, то активировать кнопку старт
        self.choice_input_file_group_box.variant_ready_signal.connect(self.control_buttons_layout.start_button_on)
        # Связь встроенных сигналов с треда
        self.simulation_thread.started.connect(self.starting_thread)
        self.simulation_thread.finished.connect(self.ending_thread)
        # Связь рукописных сигналов со слотами
        self.simulation_thread.time_signal.connect(self.progress_group_box.set_time,
                                                   Qt.QueuedConnection)
        self.simulation_thread.iteration_signal.connect(self.progress_group_box.set_iteration,
                                                        Qt.QueuedConnection)
        self.simulation_thread.ending_simulation_signal.connect(self.progress_group_box.set_time_result,
                                                                Qt.QueuedConnection)

    @pyqtSlot()
    def starting_thread(self):
        """
        При запуске потока изменяем состояние виджетов
        :return: None
        """
        self.choice_input_file_group_box.button.setEnabled(False)
        self.control_buttons_layout.start_button.setEnabled(False)
        self.control_buttons_layout.stop_button.setEnabled(True)
        self.progress_group_box.prepare_for_simulation(repeating_time_max=self.simulation_thread.variant.repeating_time,
                                                       modelling_time_max=self.simulation_thread.variant.modelling_time)

    @pyqtSlot()
    def ending_thread(self):
        """
        При окончании работы потока моделирования меняем состояние виджетов
        :return: None
        """
        self.control_buttons_layout.start_button.setEnabled(True)
        self.control_buttons_layout.stop_button.setEnabled(False)
        self.choice_input_file_group_box.button.setEnabled(True)

    @pyqtSlot()
    def start_simulate(self):
        """
        Слот при нажатии кнопки старт
        :return: None
        """
        self.simulation_thread.variant = self.choice_input_file_group_box.variant
        self.simulation_thread.start()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = StartSimulationUI()
    application.show()
    sys.exit(app.exec())
