from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt


class EquipmentLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Подключаем существующий экземпляр БД
        self.db = db

        layout = QVBoxLayout()

        # Размещение элементов
        layout.addWidget(QLabel('Список:'))
        self.equipment_layout = QHBoxLayout()
        self.equipment_table = QTableWidget()
        self.equipment_layout.addWidget(self.equipment_table, stretch=6)  # Таблица займет 6/9 пространства
        self.equipment_buttons_layout = QVBoxLayout()
        self.equipment_layout.setSpacing(25)
        self.equipment_search_button = QPushButton('Найти')
        self.equipment_insert_button = QPushButton('Добавить')
        self.equipment_update_button = QPushButton('Изменить')
        self.equipment_delete_button = QPushButton('Удалить')
        self.equipment_reset_button = QPushButton('Сбросить')
        self.equipment_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_insert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_update_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_delete_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_buttons_layout.addWidget(QLabel('Действия:'))
        self.equipment_buttons_layout.addWidget(self.equipment_search_button)
        self.equipment_buttons_layout.addWidget(self.equipment_insert_button)
        self.equipment_buttons_layout.addWidget(self.equipment_update_button)
        self.equipment_buttons_layout.addWidget(self.equipment_delete_button)
        self.equipment_buttons_layout.addWidget(self.equipment_reset_button)
        self.equipment_buttons_widget = QWidget()
        self.equipment_buttons_widget.setLayout(self.equipment_buttons_layout)
        self.equipment_buttons_widget.setFixedHeight(275)
        self.equipment_buttons_layout.setContentsMargins(50, 10, 50, 10)
        self.equipment_layout.addWidget(self.equipment_buttons_widget, stretch=3)  # Кнопки займут 3/9 пространства
        layout.addLayout(self.equipment_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

    def fill_equipment_table(self, data):
        self.equipment_table.setRowCount(len(data))
        self.equipment_table.setColumnCount(len(data[0]))
        for i in range(self.equipment_table.rowCount()):
            for j in range(self.equipment_table.columnCount()):
                item = QTableWidgetItem(str(data[i][j]))
                self.equipment_table.setItem(i, j, item)
        self.equipment_table.setColumnWidth(0, 50)
        self.equipment_table.setColumnWidth(1, 200)
        self.equipment_table.setColumnWidth(2, 200)
        self.equipment_table.setColumnWidth(3, 400)
        self.equipment_table.setColumnWidth(4, 200)
        self.equipment_table.setColumnWidth(6, 350)
        self.equipment_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.equipment_table.setHorizontalHeaderLabels(['ID',
                                                        'Наименование',
                                                        'Местоположение',
                                                        'Поставщик',
                                                        'Дата изготовления',
                                                        'Годен до',
                                                        'Ответственный'])
        self.equipment_table.verticalHeader().setVisible(False)
