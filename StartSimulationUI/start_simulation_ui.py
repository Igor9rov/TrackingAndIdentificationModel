from os import cpu_count
from queue import Queue

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QProgressBar

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

        # Список собственных потоков
        self.threads = []
        # Связь кнопки для начала моделирования
        self.control_buttons_layout.start_button.clicked.connect(self.starting_simulation)
        # Когда сделали вариант, то активировать кнопку старт
        self.choice_input_file_group_box.variant_ready_signal.connect(self.control_buttons_layout.start_button_on)
        # Если моделирование закончено
        self.progress_group_box.simulation_ending_signal.connect(self.ending_simulation)

    @pyqtSlot()
    def ending_simulation(self):
        """
        При окончании работы моделирования меняем состояние виджетов
        :return: None
        """
        self.control_buttons_layout.start_button.setEnabled(True)
        self.control_buttons_layout.stop_button.setEnabled(False)
        self.choice_input_file_group_box.button.setEnabled(True)

    @pyqtSlot()
    def starting_simulation(self):
        """
        Слот при нажатии кнопки старт моделирования
        :return: None
        """
        # Отключили кнопки.
        self.choice_input_file_group_box.button.setEnabled(False)
        self.control_buttons_layout.start_button.setEnabled(False)
        # Укажем тип варианта, чтобы потом избежать ошибок при рефакторинге
        variant: GeneratedVariant = self.choice_input_file_group_box.variant
        self.progress_group_box.prepare_for_simulation(variant.repeating_time, variant.modelling_time)
        # Обнуление собственных потоков, иначе при перезапуске добавятся ещё
        self.threads = []
        # Создадим очередь событий
        queue = Queue()
        for _ in range(variant.repeating_time):
            queue.put([variant.objects, variant.modelling_time])
        # Создаём потоки
        count_of_threads = cpu_count()
        for thread_num in range(count_of_threads):
            simulation_thread = SimulationThread(queue)
            # Нужно правильно связать каждый поток со своим прогрессбаром
            progress_bar: QProgressBar = self.progress_group_box.thread_progress_bar_list[thread_num]
            simulation_thread.time_signal.connect(progress_bar.setValue)
            # Связь с общим прогресс баром
            simulation_thread.simulation_signal.connect(self.progress_group_box.set_iteration)
            self.threads.append(simulation_thread)
        # Потоки запускаем в отдельном цикле, иначе будет вылетать
        for thread in self.threads:
            thread.start()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = StartSimulationUI()
    application.show()
    sys.exit(app.exec())
