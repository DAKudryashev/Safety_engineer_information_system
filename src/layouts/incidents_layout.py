from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt
import os


class IncidentsLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Список:'))

        # Размещение элементов
        self.incidents_layout = QHBoxLayout()
        self.incidents_table = QTableWidget()
        self.incidents_layout.addWidget(self.incidents_table, stretch=6)  # Таблица займет 6/9 пространства
        self.incidents_buttons_layout = QVBoxLayout()
        self.incidents_layout.setSpacing(25)
        self.incidents_search_button = QPushButton('Найти')
        self.incidents_insert_button = QPushButton('Добавить')
        self.incidents_update_button = QPushButton('Изменить')
        self.incidents_delete_button = QPushButton('Удалить')
        self.incidents_reset_button = QPushButton('Сбросить')
        self.incidents_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.incidents_insert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.incidents_update_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.incidents_delete_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.incidents_reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.incidents_buttons_layout.addWidget(QLabel('Действия:'))
        self.incidents_buttons_layout.addWidget(self.incidents_search_button)
        self.incidents_buttons_layout.addWidget(self.incidents_insert_button)
        self.incidents_buttons_layout.addWidget(self.incidents_update_button)
        self.incidents_buttons_layout.addWidget(self.incidents_delete_button)
        self.incidents_buttons_layout.addWidget(self.incidents_reset_button)
        self.incidents_buttons_widget = QWidget()
        self.incidents_buttons_widget.setLayout(self.incidents_buttons_layout)
        self.incidents_buttons_widget.setFixedHeight(275)
        self.incidents_buttons_layout.setContentsMargins(50, 10, 50, 10)
        self.incidents_layout.addWidget(self.incidents_buttons_widget, stretch=3)  # Кнопки займут 3/9 пространства
        layout.addLayout(self.incidents_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

    def fill_incidents_table(self, data):
        self.incidents_table.setRowCount(len(data))
        self.incidents_table.setColumnCount(len(data[0]))
        for i in range(self.incidents_table.rowCount()):
            for j in range(self.incidents_table.columnCount()):
                if j == 5:  # Если это столбец со ссылкой
                    if data[i][j] is not None:
                        btn = QPushButton("Открыть")
                        btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                        btn.clicked.connect(lambda _, path=data[i][j]: self.open_image(path))
                        # Размещаем кнопку в ячейке
                        self.incidents_table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.incidents_table.setItem(i, j, item)
                    
        self.incidents_table.setColumnWidth(0, 50)
        self.incidents_table.setColumnWidth(1, 500)
        self.incidents_table.setColumnWidth(3, 300)
        self.incidents_table.setColumnWidth(4, 300)
        self.incidents_table.setColumnWidth(5, 250)
        
        self.incidents_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.incidents_table.setHorizontalHeaderLabels(['ID',
                                                        'Содержание',
                                                        'Дата',
                                                        'Ответственный',
                                                        'Участник',
                                                        'Посмотреть фото'])
        self.incidents_table.verticalHeader().setVisible(False)

    def open_image(self, file_path):
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            print(f"Файл не найден: {file_path}")
