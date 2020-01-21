from PyQt5.QtWidgets import QVBoxLayout, QLabel, QGroupBox, QPushButton


class CPResultGroupBox(QGroupBox):
    """Виджет с кнопками с выбором результатов"""
    def __init__(self, parent=None) -> None:
        QGroupBox.__init__(self, parent)
        self.setTitle("Результаты:")

        # Нужные компоненты
        self.percent_identification_label = QLabel(text="Процент принятия решения о том,\n"
                                                        " что две трассы принадлежат одной цели: 0 %")
        self.histogram_generalized_distance_button = QPushButton(text="Гистограмма обобщённых расстояний")
        self.first_scatter_matrix_button = QPushButton(text="Scatter Matrix координат первой трассы")
        self.second_scatter_matrix_button = QPushButton(text="Scatter Matrix координат второй трассы")
        self.difference_scatter_matrix_button = QPushButton(text="Scatter Matrix разности координат трасс")
        self.first_show_diff_distribution_button = QPushButton(text="Сравнение реального и оцененного \n"
                                                                    "распределения координат первой трассы")
        self.second_show_diff_distribution_button = QPushButton(text="Сравнение реального и оцененного \n"
                                                                     "распределения координат второй трассы")

        # Основной контейнер
        layout = QVBoxLayout(self)
        layout.addWidget(self.percent_identification_label)
        layout.addWidget(self.histogram_generalized_distance_button)
        layout.addWidget(self.first_scatter_matrix_button)
        layout.addWidget(self.second_scatter_matrix_button)
        layout.addWidget(self.difference_scatter_matrix_button)
        layout.addWidget(self.first_show_diff_distribution_button)
        layout.addWidget(self.second_show_diff_distribution_button)
