from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import sys
import json

from StartingWidget import StartingWidget
from ChangeTimeParametrsWidget import ChangeTimeParametersWidget
from ChangeMFRParametersWidget import ChangeMFRParametersWidget
from ChangeTargetsParametersWidget import ChangeTargetsParametersWidget
from SaveFileWidget import SaveFileWidget


class EditVariantStackedWidget(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        QtWidgets.QStackedWidget.__init__(self, parent)

        self.starting = StartingWidget()
        self.change_time = ChangeTimeParametersWidget()
        self.change_mfr = ChangeMFRParametersWidget()
        self.change_targets = ChangeTargetsParametersWidget()
        self.save_file_widget = SaveFileWidget()

        self.addWidget(self.starting)
        self.addWidget(self.change_time)
        self.addWidget(self.change_mfr)
        self.addWidget(self.change_targets)
        self.addWidget(self.save_file_widget)

        self.starting.create_variant_button.clicked.connect(self.move_to_time_parameters_widget)

        self.change_time.next_button.clicked.connect(self.move_to_mfr_parameters_widget)
        self.change_time.back_button.clicked.connect(self.move_to_start_widget)

        self.change_mfr.next_button.clicked.connect(self.move_to_targets_parameters_widget)
        self.change_mfr.back_button.clicked.connect(self.move_to_time_parameters_widget)

        self.change_targets.back_button.clicked.connect(self.move_to_mfr_parameters_widget)
        self.change_targets.next_button.clicked.connect(self.move_to_save_variant_widget)



    @pyqtSlot()
    def move_to_time_parameters_widget(self):
        self.setCurrentWidget(self.change_time)

    @pyqtSlot()
    def move_to_mfr_parameters_widget(self):
        self.setCurrentWidget(self.change_mfr)

    @pyqtSlot()
    def move_to_start_widget(self):
        self.setCurrentWidget(self.starting)

    @pyqtSlot()
    def move_to_targets_parameters_widget(self):
        if self.change_mfr.can_press_next_button():
            self.change_targets.cancel_count_of_target_button.click()
            self.change_targets.mfr_numbers_list = self.change_mfr.numbers_checked_mfr
            self.setCurrentWidget(self.change_targets)

    @pyqtSlot()
    def move_to_save_variant_widget(self):
        if self.change_targets.can_press_next_button():
            self.setCurrentWidget(self.save_file_widget)

    @property
    def variant(self):
        return {"Time_Parameters": self.change_time.get_parameters(),
                "MFR_Parameters": self.change_mfr.get_parameters(),
                "Target_Parameters": self.change_targets.get_parameters()}

    # TODO: Доделать сохранение в json ормат варианта моделирования
    def save_file_with_variant(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = EditVariantStackedWidget()
    application.show()

    sys.exit(app.exec())
