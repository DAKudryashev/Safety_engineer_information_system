from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt


class RoomsLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Список:'))

        # Размещение элементов
        self.rooms_layout = QHBoxLayout()
        self.rooms_table = QTableWidget()
        self.rooms_layout.addWidget(self.rooms_table, stretch=4)  # Таблица займет 4/7 пространства
        self.rooms_buttons_layout = QVBoxLayout()
        self.rooms_layout.setSpacing(25)
        self.rooms_search_button = QPushButton('Найти')
        self.rooms_insert_button = QPushButton('Добавить')
        self.rooms_update_button = QPushButton('Изменить')
        self.rooms_delete_button = QPushButton('Удалить')
        self.rooms_reset_button = QPushButton('Сбросить')
        self.rooms_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_insert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_update_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_delete_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_buttons_layout.addWidget(QLabel('Действия:'))
        self.rooms_buttons_layout.addWidget(self.rooms_search_button)
        self.rooms_buttons_layout.addWidget(self.rooms_insert_button)
        self.rooms_buttons_layout.addWidget(self.rooms_update_button)
        self.rooms_buttons_layout.addWidget(self.rooms_delete_button)
        self.rooms_buttons_layout.addWidget(self.rooms_reset_button)
        self.rooms_buttons_widget = QWidget()
        self.rooms_buttons_widget.setLayout(self.rooms_buttons_layout)
        self.rooms_buttons_widget.setFixedHeight(275)
        self.rooms_buttons_layout.setContentsMargins(50, 10, 50, 10)
        self.rooms_layout.addWidget(self.rooms_buttons_widget, stretch=3)  # Кнопки займут 3/7 пространства
        layout.addLayout(self.rooms_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)
    
    def fill_rooms_table(self, data):
        self.rooms_table.setRowCount(len(data))
        self.rooms_table.setColumnCount(len(data[0]))
        for i in range(self.rooms_table.rowCount()):
            for j in range(self.rooms_table.columnCount()):
                item = QTableWidgetItem(str(data[i][j]))
                self.rooms_table.setItem(i, j, item)
        self.rooms_table.setColumnWidth(0, 80)
        self.rooms_table.setColumnWidth(1, 150)
        self.rooms_table.setColumnWidth(2, 300)
        self.rooms_table.setColumnWidth(3, 250)
        self.rooms_table.setColumnWidth(4, 500)
        self.rooms_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.rooms_table.setHorizontalHeaderLabels(['ID',
                                                    'Наименование',
                                                    'Состояние',
                                                    'Дата последней проверки',
                                                    'Ответственный'])
        self.rooms_table.verticalHeader().setVisible(False)
