from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget,
                             QPushButton, QTableWidgetItem)
from PyQt5.QtCore import Qt


class ExtraLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Применяем стилизацию
        self.setStyleSheet("""
                   QWidget {
                       background: #f5f5f5;
                   }
                   QLabel {
                       font-size: 14px;
                       color: #333;
                       padding: 5px;
                   }
                   QPushButton {
                       background: #4CAF50;
                       color: white;
                       border: none;
                       padding: 8px 16px;
                       border-radius: 4px;
                       font-size: 14px;
                       min-width: 100px;
                   }
                   QPushButton:hover {
                       background: #45a049;
                   }
                   QTableWidget {
                       background: white;
                       border: 1px solid #ddd;
                       border-radius: 4px;
                       gridline-color: #eee;
                   }
                   QHeaderView::section {
                       background: #4CAF50;
                       color: white;
                       padding: 5px;
                       border: none;
                   }
                   QScrollBar:vertical {
                       width: 12px;
                       background: #f1f1f1;
                   }
                   QScrollBar::handle:vertical {
                       background: #c1c1c1;
                       border-radius: 6px;
                   }
               """)

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

