from PyQt5.QtWidgets import QLabel, QGroupBox, QGridLayout, QCheckBox, QPushButton, QHBoxLayout, \
    QVBoxLayout


class MFRResultGroupBox(QGroupBox):
    """
    Виджет с кнопками с выбором результатов
    """
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)
        self.setTitle("Результаты:")
        # Нужные компоненты

        # Кнопки для построения графиков
        self.plot_in_one_figure_button = QPushButton(text="Построить графики в одном окне")
        self.plot_in_different_figures_button = QPushButton(text="Построить графики в разных окнах")

        # Чекбоксы для выбора графиков
        label_est = QLabel(text="Оцененные")
        label_real = QLabel(text="Реальные")
        label_other = QLabel(text="Прочее")

        self.cb_est_x = QCheckBox(text="X")
        self.cb_est_y = QCheckBox(text="Y")
        self.cb_est_z = QCheckBox(text="Z")

        self.cb_est_vx = QCheckBox(text="Vx")
        self.cb_est_vy = QCheckBox(text="Vy")
        self.cb_est_vz = QCheckBox(text="Vz")

        self.cb_est_sx = QCheckBox(text="σX")
        self.cb_est_sy = QCheckBox(text="σY")
        self.cb_est_sz = QCheckBox(text="σZ")

        self.cb_real_x = QCheckBox(text="X")
        self.cb_real_y = QCheckBox(text="Y")
        self.cb_real_z = QCheckBox(text="Z")

        self.cb_real_vx = QCheckBox(text="Vx")
        self.cb_real_vy = QCheckBox(text="Vy")
        self.cb_real_vz = QCheckBox(text="Vz")

        self.cb_real_sx = QCheckBox(text="σX")
        self.cb_real_sy = QCheckBox(text="σY")
        self.cb_real_sz = QCheckBox(text="σZ")

        self.cb_diff_x = QCheckBox(text="|ΔX|")
        self.cb_diff_y = QCheckBox(text="|ΔY|")
        self.cb_diff_z = QCheckBox(text="|ΔZ|")

        self.cb_diff_vx = QCheckBox(text="|ΔVx|")
        self.cb_diff_vy = QCheckBox(text="|ΔVy|")
        self.cb_diff_vz = QCheckBox(text="|ΔVz|")

        self.cb_ratio_sx = QCheckBox(text="σXo/σXr")
        self.cb_ratio_sy = QCheckBox(text="σYo/σYr")
        self.cb_ratio_sz = QCheckBox(text="σZo/σZr")

        # Список с checkbox нужных графиков
        widgets_list = [[label_est, label_real, label_other],
                        [self.cb_est_x, self.cb_real_x, self.cb_diff_x],
                        [self.cb_est_y, self.cb_real_y, self.cb_diff_y],
                        [self.cb_est_z, self.cb_real_z, self.cb_diff_z],
                        [self.cb_est_vx, self.cb_real_vx, self.cb_diff_vx],
                        [self.cb_est_vy, self.cb_real_vy, self.cb_diff_vy],
                        [self.cb_est_vz, self.cb_real_vz, self.cb_diff_vz],
                        [self.cb_est_sx, self.cb_real_sx, self.cb_ratio_sx],
                        [self.cb_est_sy, self.cb_real_sy, self.cb_ratio_sy],
                        [self.cb_est_sz, self.cb_real_sz, self.cb_ratio_sz]]

        # Контейнер сетки, заполним через цикл
        grid_layout = QGridLayout()
        for row_index, row in enumerate(widgets_list):
            for column_index, widget in enumerate(row):
                grid_layout.addWidget(widget, row_index, column_index)

        # Контейнер для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.plot_in_one_figure_button)
        buttons_layout.addWidget(self.plot_in_different_figures_button)

        # Основной контейнер
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(buttons_layout)
