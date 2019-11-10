from PyQt5.QtWidgets import QHBoxLayout

from target_velocity_line_edit import TargetVelocityLineEdit


class TargetVelocitiesBoxLayout(QHBoxLayout):
    """Контейнер с вводом всех скоростей цели"""
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)
        # Основные компоненты
        self.velocity_lines_edit = [TargetVelocityLineEdit(f"{coord}") for coord in ["x", "y", "z"]]
        # Добавим их в контейнер
        for line_edit in self.velocity_lines_edit:
            self.addWidget(line_edit)

    def can_get_velocities(self) -> bool:
        """Попытка получения скоростей

        :return: True/False в зависимости от того, ввёл ли пользователь скорости
        :rtype: bool
        """
        try:
            _ = self.velocities
        except ValueError:
            return False
        return True

    @property
    def velocities(self) -> list:
        """Скорость цели

        :raise: ValueError если пользователь не ввёл скорость хотя бы по одной координате
        :return: Список из скоростей цели по каждой координате
        :rtype: list
        """
        return [float(line_edit.text()) for line_edit in self.velocity_lines_edit]

    @velocities.setter
    def velocities(self, new_velocities: list):
        """Устанавливает скорости цели

        :param new_velocities: Список из скоростей цели по каждой координате
        :type new_velocities: list

        :return: None
        """
        for index, line_edit in enumerate(self.velocity_lines_edit):
            line_edit.setText(str(new_velocities[index]))
