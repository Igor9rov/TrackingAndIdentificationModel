from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTreeView, QAbstractItemView, QHeaderView

from layout_with_back_and_next_buttons import LayoutWithBackAndNextButtons


# Виджет для сохранения в файл
class SaveFileWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.layout = QVBoxLayout(self)
        # Хотим посмотреть на вариант моделирования
        self.group_box = QGroupBox("Получившийся вариант моделирования")
        self.layout.addWidget(self.group_box)

        self.group_box_layout = QVBoxLayout(self.group_box)
        # Вывод варианта моделирования в виде иерархического дерева
        self.variant_tree_view = QTreeView()
        self.group_box_layout.addWidget(self.variant_tree_view)
        # Не хотим его редактировать
        self.variant_tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Ссылка на экземпляр класса, упарвляющего заголовком
        header = self.variant_tree_view.header()
        # Задание режима для изменения размеров секций
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # Модель представления данных
        self.model = QStandardItemModel(self)
        self.variant_tree_view.setModel(self.model)
        # Нижний контейнер
        self.lower_layout = LayoutWithBackAndNextButtons()
        self.layout.addLayout(self.lower_layout)
        # Для удобного доступа
        self.save_file_button = self.lower_layout.next_button
        self.back_button = self.lower_layout.back_button

        self.save_file_button.setText("Сохранить вариант моделирования")
