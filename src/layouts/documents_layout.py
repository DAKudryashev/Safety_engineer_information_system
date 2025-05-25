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
        self.regulatory_layout.addWidget(self.regulatory_table, stretch=6)  # Таблица займет 6/7 пространства
        self.regulatory_buttons_layout = QVBoxLayout()
        self.reg_search_button = QPushButton('Поиск')
        self.reg_insert_button = QPushButton('Добавить')
        self.reg_update_button = QPushButton('Изменить')
        self.reg_delete_button = QPushButton('Удалить')
        self.reg_reset_button = QPushButton('Сбросить')
        self.regulatory_buttons_layout.addWidget(QLabel('Действия:'))
        self.regulatory_buttons_layout.addWidget(self.reg_search_button)
        self.regulatory_buttons_layout.addWidget(self.reg_insert_button)
        self.regulatory_buttons_layout.addWidget(self.reg_update_button)
        self.regulatory_buttons_layout.addWidget(self.reg_delete_button)
        self.regulatory_buttons_layout.addWidget(self.reg_reset_button)
        self.reg_buttons_widget = QWidget()
        self.reg_buttons_widget.setLayout(self.regulatory_buttons_layout)
        self.reg_buttons_widget.setFixedHeight(260)
        self.regulatory_layout.addWidget(self.reg_buttons_widget, stretch=1)  # Кнопки займут 1/7 пространства
        layout.addLayout(self.regulatory_layout)

        layout.addWidget(QLabel('Внутренние документы:'))

        # Размещение элементов для внутренних документов
        self.internal_layout = QHBoxLayout()
        self.internal_table = QTableWidget()
        self.internal_layout.addWidget(self.internal_table, stretch=6)  # Таблица займет 6/7 пространства
        self.internal_buttons_layout = QVBoxLayout()
        self.inter_search_button = QPushButton('Поиск')
        self.inter_insert_button = QPushButton('Добавить')
        self.inter_update_button = QPushButton('Изменить')
        self.inter_delete_button = QPushButton('Удалить')
        self.inter_reset_button = QPushButton('Сбросить')
        self.internal_buttons_layout.addWidget(QLabel('Действия:'))
        self.internal_buttons_layout.addWidget(self.inter_search_button)
        self.internal_buttons_layout.addWidget(self.inter_insert_button)
        self.internal_buttons_layout.addWidget(self.inter_update_button)
        self.internal_buttons_layout.addWidget(self.inter_delete_button)
        self.internal_buttons_layout.addWidget(self.inter_reset_button)
        self.inter_buttons_widget = QWidget()
        self.inter_buttons_widget.setLayout(self.internal_buttons_layout)
        self.inter_buttons_widget.setFixedHeight(260)
        self.internal_layout.addWidget(self.inter_buttons_widget, stretch=1)  # Кнопки займут 1/7 пространства
        layout.addLayout(self.internal_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)
        
    def fill_regulatory_table(self, data):
        self.regulatory_table.setRowCount(len(data))
        self.regulatory_table.setColumnCount(len(data[0]))
        for i in range(self.regulatory_table.rowCount()):
            for j in range(self.regulatory_table.columnCount()):
                if j == 3:  # Если это столбец со ссылкой
                    btn = QPushButton("Открыть")
                    btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                    btn.clicked.connect(lambda _, url=data[i][j]: webbrowser.open(url))
                    # Размещаем кнопку в ячейке
                    self.regulatory_table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.regulatory_table.setItem(i, j, item)
        self.regulatory_table.setColumnWidth(0, 50)
        self.regulatory_table.setColumnWidth(1, 1500)
        self.regulatory_table.setColumnWidth(3, 300)
        self.regulatory_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.regulatory_table.setHorizontalHeaderLabels(['ID',
                                                         'Название',
                                                         'Дата создания',
                                                         'Посмотреть содержание'])
        self.regulatory_table.verticalHeader().setVisible(False)

    def fill_internal_table(self, data):
        self.internal_table.setRowCount(len(data))
        self.internal_table.setColumnCount(len(data[0]))
        for i in range(self.internal_table.rowCount()):
            for j in range(self.internal_table.columnCount()):
                if j == 4:  # Если это столбец со ссылкой
                    btn = QPushButton("Открыть")
                    btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                    btn.clicked.connect(lambda _, path=data[i][j]: self.open_pdf(path))
                    # Размещаем кнопку в ячейке
                    self.internal_table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.internal_table.setItem(i, j, item)
        self.internal_table.setColumnWidth(0, 50)
        self.internal_table.setColumnWidth(1, 1200)
        self.internal_table.setColumnWidth(3, 350)
        self.internal_table.setColumnWidth(4, 250)
        self.internal_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.internal_table.setHorizontalHeaderLabels(['ID',
                                                       'Название',
                                                       'Дата создания',
                                                       'Добавил',
                                                       'Посмотреть содержание'])
        self.internal_table.verticalHeader().setVisible(False)

    def open_pdf(self, file_path):
        """Открывает PDF-файл программой по умолчанию"""
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            print(f"Файл не найден: {file_path}")
