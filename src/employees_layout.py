from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class EmployeesLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Содержимое слоя'))

        # Закрепление слоя на вкладке
        self.setLayout(layout)
