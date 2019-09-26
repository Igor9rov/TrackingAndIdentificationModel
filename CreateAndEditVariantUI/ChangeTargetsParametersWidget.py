from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QCheckBox, QRadioButton, QApplication, QSpinBox, QTabWidget
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from LayoutWithBackAndNextButtons import LayoutWithBackAndNextButtons
from ErrorMessageBox import ErrorMessageBox
import sys


# Группа параметров целей, связанных с МФР
class TargetGroupBoxParametersAssociatedWithMFR(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self, "Сопровождение этим МФР", parent)
        self.setCheckable(True)
        self.anj_check_box = QCheckBox("Постановщик АШП")
        self.auto_tracking_check_box = QCheckBox("Точное АС")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.anj_check_box)
        self.layout.addWidget(self.auto_tracking_check_box)

    # Получение параметров, связанных с МФР
    def get_parameters(self):
        return {"Tracked": self.isChecked(),
                "IsAnj": self.anj_check_box.isChecked(),
                "IsAutoTracking": self.auto_tracking_check_box.isChecked()}


# Поле для ввода координат цели
class TargetCoordinateLineEdit(QLineEdit):
    def __init__(self, coordinate="x", parent=None):
        QLineEdit.__init__(self, parent)
        max_value_dict = {"x": 150000, "y": 20000, "z": 150000}
        max_value_dict.setdefault(coordinate, 1)
        min_value_dict = {"x": -150000, "y": 0, "z": -150000}
        min_value_dict.setdefault(coordinate, 0)
        validator = QIntValidator()
        validator.setRange(min_value_dict[coordinate], max_value_dict[coordinate])
        self.setValidator(validator)


# Поле для ввода скоростей целей
class TargetVelocityLineEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        max_velocity = 700
        min_velocity = -700
        validator = QIntValidator()
        validator.setRange(min_velocity, max_velocity)
        self.setValidator(validator)


# Контейнер с вводом всех трёх координат цели
class TargetCoordinatesBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)
        self.x_coordinate_line_edit = TargetCoordinateLineEdit("x")
        self.addWidget(self.x_coordinate_line_edit)
        self.y_coordinate_line_edit = TargetCoordinateLineEdit("y")
        self.addWidget(self.y_coordinate_line_edit)
        self.z_coordinate_line_edit = TargetCoordinateLineEdit("z")
        self.addWidget(self.z_coordinate_line_edit)

    # Попытка получения координат
    def can_get_coordinates(self):
        try:
            coordinates = self.coordinates
        except ValueError:
            return False
        return True

    # Координаты
    @property
    def coordinates(self):
        return [float(self.x_coordinate_line_edit.text()),
                float(self.y_coordinate_line_edit.text()),
                float(self.z_coordinate_line_edit.text())]


# Контейнер с вводом всех трёх скоростей цели
class TargetVelocitiesBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)
        self.x_velocity_line_edit = TargetVelocityLineEdit()
        self.addWidget(self.x_velocity_line_edit)

        self.y_velocity_line_edit = TargetVelocityLineEdit()
        self.addWidget(self.y_velocity_line_edit)

        self.z_velocity_line_edit = TargetVelocityLineEdit()
        self.addWidget(self.z_velocity_line_edit)

    # Попытка получения скоростей
    def can_get_velocities(self):
        try:
            velocities = self.velocities
        except ValueError:
            return False
        return True

    # Скорость
    @property
    def velocities(self):
        return [float(self.x_velocity_line_edit.text()),
                float(self.y_velocity_line_edit.text()),
                float(self.z_velocity_line_edit.text())]


# Контейнер для ввода типа цели
class TargetTypeBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)

        self.aerodynamic_radio_button = QRadioButton("Аэродинамическая цель")
        self.aerodynamic_radio_button.setChecked(True)
        self.ballistic_radio_button = QRadioButton("Баллистическая цель")

        self.addWidget(self.aerodynamic_radio_button)
        self.addWidget(self.ballistic_radio_button)

    @property
    def type(self):
        return "Aerodynamic" if self.aerodynamic_radio_button.isChecked() else "Ballistic"


# Виджет для редактирования параметров одной цели, появляется в таблице
class TargetParametersWidget(QWidget):
    def __init__(self, number_target: int, mfr_numbers: list, parent=None):
        QWidget.__init__(self, parent)
        self.number_target = number_target
        self.mfr_numbers = mfr_numbers

        self.coordinates_box = TargetCoordinatesBoxLayout()
        self.velocities_box = TargetVelocitiesBoxLayout()
        self.target_type_box = TargetTypeBoxLayout()

        self.form_layout = QFormLayout(self)
        self.form_layout.addRow("Координаты:", self.coordinates_box)
        self.form_layout.addRow("Скорость:", self.velocities_box)
        self.form_layout.addRow("Тип цели:", self.target_type_box)

        self.mfr_parameters_widgets = [TargetGroupBoxParametersAssociatedWithMFR() for _ in self.mfr_numbers]
        # Для каждого из МФР добавить виджет с редактированием его параметров
        for mfr_number, mfr_parameters_widget in zip(self.mfr_numbers, self.mfr_parameters_widgets):
            self.form_layout.addRow(f"МФР №{mfr_number}:", mfr_parameters_widget)

    @property
    def has_coordinates(self):
        return self.coordinates_box.can_get_coordinates()

    @property
    def has_velocities(self):
        return self.velocities_box.can_get_velocities()

    def get_mfr_parameters(self):
        return dict(zip(self.mfr_numbers, [widget.get_parameters()for widget in self.mfr_parameters_widgets]))

    # Получение параметров одной цели
    def get_parameters(self):
        return {"Coordinates": self.coordinates_box.coordinates,
                "Velocities": self.velocities_box.velocities,
                "Type": self.target_type_box.type,
                "MFRParameters": self.get_mfr_parameters()}


# Основной виджет, содержит кнопки управления и таблицу с редактированием параметров цели
class ChangeTargetsParametersWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.mfr_numbers_list = []

        self.set_target_number_line = QLabel("Укажите количество целей")
        self.min_count_of_target = 1
        self.max_count_of_target = 10
        self.number_spin_box = QSpinBox()
        self.number_spin_box.setRange(self.min_count_of_target, self.max_count_of_target)
        self.accept_count_of_target_button = QPushButton("Изменить их параметры")
        self.cancel_count_of_target_button = QPushButton("Удалить все цели, начать ввод заново")

        self.set_numbers_hbox = QHBoxLayout()
        self.set_numbers_hbox.addWidget(self.set_target_number_line)
        self.set_numbers_hbox.addWidget(self.number_spin_box)
        self.set_numbers_hbox.addWidget(self.accept_count_of_target_button)
        self.set_numbers_hbox.addWidget(self.cancel_count_of_target_button)

        self.target_parameters_tab = QTabWidget()

        self.layout_with_next_and_back_buttons = LayoutWithBackAndNextButtons()

        self.main_box = QVBoxLayout(self)
        self.main_box.addLayout(self.set_numbers_hbox)
        self.main_box.addWidget(self.target_parameters_tab)
        self.main_box.addLayout(self.layout_with_next_and_back_buttons)

        # Это для более удобного обращения к ним
        self.next_button = self.layout_with_next_and_back_buttons.next_button
        self.back_button = self.layout_with_next_and_back_buttons.back_button

        self.accept_count_of_target_button.clicked.connect(self.clicked_on_accept_target_number_button)
        self.cancel_count_of_target_button.clicked.connect(self.clicked_on_cancel_target_number_button)

        self.cancel_count_of_target_button.setEnabled(False)
        self.next_button.setEnabled(False)

    # Получение параметров целей
    def get_parameters(self):
        return dict(zip(range(self.number_spin_box.value()),
                        [tab.get_parameters() for tab in self._all_tab_with_target_parameters]))

    # Все вкладки таблицы с параметрами цели
    @property
    def _all_tab_with_target_parameters(self):
        return [self.target_parameters_tab.widget(index) for index in range(self.target_parameters_tab.count())]

    # Слот для отрисовки таблицы с параметрами для каждой цели
    @pyqtSlot()
    def clicked_on_accept_target_number_button(self):
        self.accept_count_of_target_button.setEnabled(False)
        self.cancel_count_of_target_button.setEnabled(True)
        self.next_button.setEnabled(True)
        self.number_spin_box.setReadOnly(True)
        for number_target in range(self.number_spin_box.value()):
            self.target_parameters_tab.addTab(TargetParametersWidget(number_target, self.mfr_numbers_list),
                                              f"Цель №{number_target}")

    # Слот для очищения таблицы
    @pyqtSlot()
    def clicked_on_cancel_target_number_button(self):
        self.cancel_count_of_target_button.setEnabled(False)
        self.accept_count_of_target_button.setEnabled(True)
        self.next_button.setEnabled(False)
        self.number_spin_box.setReadOnly(False)
        self.number_spin_box.setValue(self.min_count_of_target)
        self.target_parameters_tab.clear()

    # Можно ли нажать кнопку далее (сгенерировать вариант моделирования)
    def can_press_next_button(self):
        if self._processing_all_targets_has_coordinates():
            return self._processing_all_targets_has_velocities()
        return False

    # Обработка того, что все цели имеют координаты
    def _processing_all_targets_has_coordinates(self):
        return self._all_targets_has_coordinates() or self.processing_message_about_lack_of_coordinates()

    # У всех целей есть координаты
    def _all_targets_has_coordinates(self):
        return all([widget.has_coordinates for widget in self._all_tab_with_target_parameters])

    # Обработка сообщения о том, что у целей нет координат
    def processing_message_about_lack_of_coordinates(self):
        self.show_message_about_lack_of_coordinates()
        return False

    # Вывод сообщения о том, что у целей отсутсвуют координаты
    def show_message_about_lack_of_coordinates(self):
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Отсутсвуют координаты у целей")
        message_box.exec()

    # Обработка того, что все цели имеют скорости
    def _processing_all_targets_has_velocities(self):
        return self._all_targets_has_velocities() or self.processing_message_about_lack_of_velocities()

    # У всех целей есть скорость
    def _all_targets_has_velocities(self):
        return all([widget.has_velocities for widget in self._all_tab_with_target_parameters])

    # Обработка сообщения о том, что у целей нет скорости
    def processing_message_about_lack_of_velocities(self):
        self.show_message_about_lack_of_velocities()
        return False

    # Вывод сообщения о том, что у целей отсутсвуют скорости
    def show_message_about_lack_of_velocities(self):
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Отсутсвуют скорости у целей")
        message_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = ChangeTargetsParametersWidget()
    application.show()
    sys.exit(app.exec())
