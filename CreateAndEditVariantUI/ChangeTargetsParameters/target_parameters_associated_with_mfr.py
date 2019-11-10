from PyQt5.QtWidgets import QGroupBox, QCheckBox, QVBoxLayout

from structure_of_variant import KeyMFRForTarget


class TargetParametersAssociatedWithMFR(QGroupBox):
    """Группа параметров целей, связанных с МФР"""
    def __init__(self, parent=None, number: str = "0"):
        QGroupBox.__init__(self, "Сопровождение этим МФР", parent)
        # Сохранение номера МФП
        self.number = number
        # Основные компоненты
        self.anj_check_box = QCheckBox("Постановщик АШП")
        self.auto_tracking_check_box = QCheckBox("Точное АС")
        # Основной контейнер
        layout = QVBoxLayout(self)
        layout.addWidget(self.anj_check_box)
        layout.addWidget(self.auto_tracking_check_box)

        self.setCheckable(True)

    @property
    def parameters(self) -> dict:
        """
        :return: Получение параметров, связанных с МФР
        :rtype: dict
        """
        return {KeyMFRForTarget.tracked: self.isChecked(),
                KeyMFRForTarget.is_anj: self.anj_check_box.isChecked(),
                KeyMFRForTarget.is_auto_tracking: self.auto_tracking_check_box.isChecked()}

    @parameters.setter
    def parameters(self, new_parameters: dict):
        """Установка параметров цели, связанных с МФР

        :param new_parameters: Словарь параметров
        :type new_parameters: dict

        :return: None
        """
        self.setChecked(new_parameters[KeyMFRForTarget.tracked])
        self.anj_check_box.setChecked(new_parameters[KeyMFRForTarget.is_anj])
        self.auto_tracking_check_box.setChecked(new_parameters[KeyMFRForTarget.is_auto_tracking])
