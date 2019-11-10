from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTreeView, QAbstractItemView, QHeaderView

from layout_with_back_and_next_buttons import LayoutWithBackAndNextButtons


class SaveFileWidget(QWidget):
    """Виджет для сохранения в файл"""
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Основные компоненты
        # Вывод варианта моделирования в виде иерархического дерева
        variant_tree_view = QTreeView()
        # Не хотим пользователю дать разрешение на его редактирование
        variant_tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Ссылка на экземпляр класса, управляющего заголовком
        header = variant_tree_view.header()
        # Задание режима для изменения размеров секций (автоматически растягивается)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # Модель представления данных
        self.model = QStandardItemModel(self)
        variant_tree_view.setModel(self.model)

        # Групбокс с вариантом моделирования
        group_box = QGroupBox("Получившийся вариант моделирования")
        group_box_layout = QVBoxLayout(group_box)
        group_box_layout.addWidget(variant_tree_view)
        # Контейнер с кнопками назад/далее
        control_layout = LayoutWithBackAndNextButtons()

        # Основной контейнер
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(group_box)
        main_layout.addLayout(control_layout)
        # Для удобного доступа
        self.save_file_button = control_layout.next_button
        self.back_button = control_layout.back_button
        # Изменим надпись на кнопке на подходящую
        self.save_file_button.setText("Сохранить вариант моделирования")
