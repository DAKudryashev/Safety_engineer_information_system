from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt


class ComplaintsLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Подключаем существующий экземпляр БД
        self.db = db

        layout = QVBoxLayout()

        # Размещение элементов
        layout.addWidget(QLabel('Список:'))
        self.complaints_layout = QHBoxLayout()
        self.complaints_table = QTableWidget()
        self.complaints_layout.addWidget(self.complaints_table, stretch=6)  # Таблица займет 6/9 пространства
        self.complaints_buttons_layout = QVBoxLayout()
        self.complaints_layout.setSpacing(25)
        self.complaints_search_button = QPushButton('Найти')
        self.complaints_insert_button = QPushButton('Добавить')
        self.complaints_update_button = QPushButton('Изменить')
        self.complaints_delete_button = QPushButton('Удалить')
        self.complaints_reset_button = QPushButton('Сбросить')
        self.complaints_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.complaints_insert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.complaints_update_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.complaints_delete_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.complaints_reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.complaints_buttons_layout.addWidget(QLabel('Действия:'))
        self.complaints_buttons_layout.addWidget(self.complaints_search_button)
        self.complaints_buttons_layout.addWidget(self.complaints_insert_button)
        self.complaints_buttons_layout.addWidget(self.complaints_update_button)
        self.complaints_buttons_layout.addWidget(self.complaints_delete_button)
        self.complaints_buttons_layout.addWidget(self.complaints_reset_button)
        self.complaints_buttons_widget = QWidget()
        self.complaints_buttons_widget.setLayout(self.complaints_buttons_layout)
        self.complaints_buttons_widget.setFixedHeight(275)
        self.complaints_buttons_layout.setContentsMargins(50, 10, 50, 10)
        self.complaints_layout.addWidget(self.complaints_buttons_widget, stretch=3)  # Кнопки займут 3/9 пространства
        layout.addLayout(self.complaints_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

    def fill_complaints_table(self, data):
        self.complaints_table.setRowCount(len(data))
        self.complaints_table.setColumnCount(len(data[0]))
        for i in range(self.complaints_table.rowCount()):
            for j in range(self.complaints_table.columnCount()):
                item = QTableWidgetItem(str(data[i][j]))
                self.complaints_table.setItem(i, j, item)

        self.complaints_table.setColumnWidth(0, 50)
        self.complaints_table.setColumnWidth(1, 300)
        self.complaints_table.setColumnWidth(2, 550)
        self.complaints_table.setColumnWidth(4, 200)
        self.complaints_table.setColumnWidth(5, 300)

        self.complaints_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.complaints_table.setHorizontalHeaderLabels(['ID',
                                                         'Автор',
                                                         'Содержание',
                                                         'Дата',
                                                         'Статус',
                                                         'Ответственный'])
        self.complaints_table.verticalHeader().setVisible(False)
