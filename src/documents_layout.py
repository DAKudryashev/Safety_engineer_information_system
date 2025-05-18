from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt
import webbrowser
import os


class DocumentsLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Регулирующие документы:'))

        # Размещение элементов для регулирующий документов
        self.regulatory_layout = QHBoxLayout()
        self.regulatory_table = QTableWidget()
        self.regulatory_layout.addWidget(self.regulatory_table)
        self.regulatory_buttons_layout = QVBoxLayout()
        self.reg_insert_button = QPushButton('Добавить')
        self.reg_update_button = QPushButton('Изменить')
        self.reg_delete_button = QPushButton('Удалить')
        self.regulatory_buttons_layout.addWidget(self.reg_insert_button)
        self.regulatory_buttons_layout.addWidget(self.reg_update_button)
        self.regulatory_buttons_layout.addWidget(self.reg_delete_button)
        self.regulatory_layout.addLayout(self.regulatory_buttons_layout)
        layout.addLayout(self.regulatory_layout)

        layout.addWidget(QLabel('Внутренние документы:'))

        # Размещение элементов для внутренних документов
        self.internal_layout = QHBoxLayout()
        self.internal_table = QTableWidget()
        self.internal_layout.addWidget(self.internal_table)
        self.internal_buttons_layout = QVBoxLayout()
        self.inter_insert_button = QPushButton('Добавить')
        self.inter_update_button = QPushButton('Изменить')
        self.inter_delete_button = QPushButton('Удалить')
        self.internal_buttons_layout.addWidget(self.inter_insert_button)
        self.internal_buttons_layout.addWidget(self.inter_update_button)
        self.internal_buttons_layout.addWidget(self.inter_delete_button)
        self.internal_layout.addLayout(self.internal_buttons_layout)
        layout.addLayout(self.internal_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)
        
    def fill_regulatory_table(self, data):
        self.regulatory_table.setRowCount(len(data))
        self.regulatory_table.setColumnCount(len(data[0]))
        for i in range(self.regulatory_table.rowCount()):
            for j in range(self.regulatory_table.columnCount()):
                if j == 2:  # Если это столбец со ссылкой
                    btn = QPushButton("Открыть")
                    btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                    btn.clicked.connect(lambda _, url=data[i][j]: webbrowser.open(url))
                    # Размещаем кнопку в ячейке
                    self.regulatory_table.setCellWidget(i, j, btn)
                else:
                    item = QTableWidgetItem(data[i][j])
                    self.regulatory_table.setItem(i, j, item)
        self.regulatory_table.setColumnWidth(0, 1500)
        self.regulatory_table.setColumnWidth(2, 300)
        self.regulatory_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.regulatory_table.setHorizontalHeaderLabels(['Название', 'Дата создания', 'Посмотреть содержание'])

    def fill_internal_documents(self, data):
        self.internal_table.setRowCount(len(data))
        self.internal_table.setColumnCount(len(data[0]))
        for i in range(self.internal_table.rowCount()):
            for j in range(self.internal_table.columnCount()):
                if j == 3:  # Если это столбец со ссылкой
                    btn = QPushButton("Открыть")
                    btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                    btn.clicked.connect(lambda _, path=data[i][j]: webbrowser.open(path))
                    # Размещаем кнопку в ячейке
                    self.internal_table.setCellWidget(i, j, btn)
                else:
                    item = QTableWidgetItem(data[i][j])
                    self.internal_table.setItem(i, j, item)
        self.internal_table.setColumnWidth(0, 1500)
        self.internal_table.setColumnWidth(2, 350)
        self.internal_table.setColumnWidth(3, 250)
        self.internal_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.internal_table.setHorizontalHeaderLabels(['Название', 'Дата создания', 'Добавил', 'Посмотреть содержание'])

    def open_pdf(self, file_path):
        """Открывает PDF-файл программой по умолчанию"""
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            print(f"Файл не найден: {file_path}")
