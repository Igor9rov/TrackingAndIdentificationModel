from PyQt5.QtWidgets import QHBoxLayout

from target_velocity_spin_box import TargetVelocitySpinBox


class TargetVelocitiesBoxLayout(QHBoxLayout):
    """Контейнер с вводом всех скоростей цели"""
    def __init__(self, parent=None) -> None:
        QHBoxLayout.__init__(self, parent)
        # Основные компоненты
        self.velocity_spin_boxes = [TargetVelocitySpinBox(coord) for coord in ["x", "y", "z"]]
        # Добавим их в контейнер
        for spin_box in self.velocity_spin_boxes:
            self.addWidget(spin_box)

    @property
    def velocities(self) -> list:
        """Скорость цели

        :return: Список из скоростей цели по каждой координате
        :rtype: list
        """
        return [spin_box.value() for spin_box in self.velocity_spin_boxes]

    @velocities.setter
    def velocities(self, new_velocities: list) -> None:
        """Устанавливает скорости цели

        :param new_velocities: Список из скоростей цели по каждой координате
        :type new_velocities: list

        :return: None
        """
        for index, spin_box in enumerate(self.velocity_spin_boxes):
            spin_box.setValue(new_velocities[index])
