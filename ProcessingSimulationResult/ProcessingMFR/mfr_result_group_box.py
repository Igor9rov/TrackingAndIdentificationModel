from PyQt5.QtWidgets import QLabel, QGroupBox, QGridLayout, QApplication, QCheckBox


class MFRResultGroupBox(QGroupBox):
    """
    Виджет с кнопками с выбором результатов
    """
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)
        self.setTitle("Результаты:")
        # TODO: Сделать по-человечески, через цикл
        # Нужные компоненты
        label_est = QLabel(text="Оцененные")
        label_real = QLabel(text="Реальные")
        label_other = QLabel(text="Прочее")

        cb_est_x = QCheckBox(text="X")
        cb_est_y = QCheckBox(text="Y")
        cb_est_z = QCheckBox(text="Z")

        cb_est_vx = QCheckBox(text="Vx")
        cb_est_vy = QCheckBox(text="Vy")
        cb_est_vz = QCheckBox(text="Vz")

        cb_est_sx = QCheckBox(text="Sigma X")
        cb_est_sy = QCheckBox(text="Sigma Y")
        cb_est_sz = QCheckBox(text="Sigma Z")

        cb_real_x = QCheckBox(text="X")
        cb_real_y = QCheckBox(text="Y")
        cb_real_z = QCheckBox(text="Z")

        cb_real_vx = QCheckBox(text="Vx")
        cb_real_vy = QCheckBox(text="Vy")
        cb_real_vz = QCheckBox(text="Vz")

        cb_real_sx = QCheckBox(text="Sigma X")
        cb_real_sy = QCheckBox(text="Sigma Y")
        cb_real_sz = QCheckBox(text="Sigma Z")

        # Основной контейнер
        grid = QGridLayout(self)
        grid.addWidget(label_est, 0, 0)
        grid.addWidget(label_real, 0, 1)
        grid.addWidget(label_other, 0, 2)

        grid.addWidget(cb_est_x, 1, 0)
        grid.addWidget(cb_est_y, 2, 0)
        grid.addWidget(cb_est_z, 3, 0)

        grid.addWidget(cb_est_vx, 4, 0)
        grid.addWidget(cb_est_vy, 5, 0)
        grid.addWidget(cb_est_vz, 6, 0)

        grid.addWidget(cb_est_sx, 7, 0)
        grid.addWidget(cb_est_sy, 8, 0)
        grid.addWidget(cb_est_sz, 9, 0)

        grid.addWidget(cb_real_x, 1, 1)
        grid.addWidget(cb_real_y, 2, 1)
        grid.addWidget(cb_real_z, 3, 1)

        grid.addWidget(cb_real_vx, 4, 1)
        grid.addWidget(cb_real_vy, 5, 1)
        grid.addWidget(cb_real_vz, 6, 1)

        grid.addWidget(cb_real_sx, 7, 1)
        grid.addWidget(cb_real_sy, 8, 1)
        grid.addWidget(cb_real_sz, 9, 1)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = MFRResultGroupBox()
    application.show()
    sys.exit(app.exec())

