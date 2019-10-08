from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QHBoxLayout, QApplication


class ChoiceMode(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        label = QLabel(text="Выберите режим:")
        self.mode_spin_box = QComboBox()
        self.mode_spin_box.addItem("усреднение по всем реализациям")
        self.mode_spin_box.addItem("конкретная реализация")

        layout = QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.mode_spin_box)

        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = ChoiceMode()
    application.show()
    sys.exit(app.exec())
