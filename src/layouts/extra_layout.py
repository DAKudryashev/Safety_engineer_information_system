from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget,
                             QPushButton, QTableWidgetItem)
from PyQt5.QtCore import Qt


class ExtraLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Размещение элементов
        layout.addWidget(QLabel('Сохранить все и выйти:'))
        self.escape_button = QPushButton('Выход')
        layout.addWidget(self.escape_button)
        layout.addWidget(QLabel('Список инженеров по ТБ:'))
        self.engineers_table = QTableWidget()
        layout.addWidget(self.engineers_table)
        layout.setContentsMargins(10, 10, 2100, 800)
        
        # Закрепление слоя на вкладке
        self.setLayout(layout)

    def fill_engineers_table(self, data):
        self.engineers_table.setRowCount(len(data))
        self.engineers_table.setColumnCount(len(data[0]))
        for i in range(self.engineers_table.rowCount()):
            for j in range(self.engineers_table.columnCount()):
                item = QTableWidgetItem(str(data[i][j]))
                self.engineers_table.setItem(i, j, item)
        self.engineers_table.setColumnWidth(0, 50)
        self.engineers_table.setColumnWidth(1, 300)
        self.engineers_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.engineers_table.setHorizontalHeaderLabels(['ID',
                                                        'ФИО'])
        self.engineers_table.verticalHeader().setVisible(False)

