from PyQt5.QtWidgets import QGroupBox, QCheckBox, QVBoxLayout

from structure_of_variant import KeyMFRForTarget


# Группа параметров целей, связанных с МФР
class TargetParametersAssociatedWithMFR(QGroupBox):
    def __init__(self, parent=None, number="0"):
        QGroupBox.__init__(self, "Сопровождение этим МФР", parent)
        self.setCheckable(True)
        self.number = number
        self.anj_check_box = QCheckBox("Постановщик АШП")
        self.auto_tracking_check_box = QCheckBox("Точное АС")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.anj_check_box)
        self.layout.addWidget(self.auto_tracking_check_box)

    # Получение параметров, связанных с МФР
    @property
    def parameters(self):
        return {KeyMFRForTarget.tracked: self.isChecked(),
                KeyMFRForTarget.is_anj: self.anj_check_box.isChecked(),
                KeyMFRForTarget.is_auto_tracking: self.auto_tracking_check_box.isChecked()}

    @parameters.setter
    def parameters(self, new_parameters: dict):
        self.setChecked(new_parameters[KeyMFRForTarget.tracked])
        self.anj_check_box.setChecked(new_parameters[KeyMFRForTarget.is_anj])
        self.auto_tracking_check_box.setChecked(new_parameters[KeyMFRForTarget.is_auto_tracking])
