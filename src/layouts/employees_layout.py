from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt


class EmployeesLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Список:'))

        # Размещение элементов
        self.employees_layout = QHBoxLayout()
        self.employees_table = QTableWidget()
        self.employees_layout.addWidget(self.employees_table, stretch=6)  # Таблица займет 6/9 пространства
        self.employees_buttons_layout = QVBoxLayout()
        self.employees_layout.setSpacing(25)
        self.employees_search_button = QPushButton('Найти')
        self.employees_insert_button = QPushButton('Добавить')
        self.employees_update_button = QPushButton('Изменить')
        self.employees_delete_button = QPushButton('Удалить')
        self.employees_reset_button = QPushButton('Сбросить')
        self.employees_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.employees_insert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.employees_update_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.employees_delete_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.employees_reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.employees_buttons_layout.addWidget(QLabel('Действия:'))
        self.employees_buttons_layout.addWidget(self.employees_search_button)
        self.employees_buttons_layout.addWidget(self.employees_insert_button)
        self.employees_buttons_layout.addWidget(self.employees_update_button)
        self.employees_buttons_layout.addWidget(self.employees_delete_button)
        self.employees_buttons_layout.addWidget(self.employees_reset_button)
        self.employees_buttons_widget = QWidget()
        self.employees_buttons_widget.setLayout(self.employees_buttons_layout)
        self.employees_buttons_widget.setFixedHeight(275)
        self.employees_buttons_layout.setContentsMargins(50, 10, 50, 10)
        self.employees_layout.addWidget(self.employees_buttons_widget, stretch=3)  # Кнопки займут 3/7 пространства
        layout.addLayout(self.employees_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)
    
    def fill_employees_table(self, data):
        self.employees_table.setRowCount(len(data))
        self.employees_table.setColumnCount(len(data[0]))
        for i in range(self.employees_table.rowCount()):
            for j in range(self.employees_table.columnCount()):
                if j == 0:
                    item = QTableWidgetItem(str(data[i][j]))
                else:
                    item = QTableWidgetItem(data[i][j])
                self.employees_table.setItem(i, j, item)

        self.employees_table.setColumnWidth(0, 50)
        self.employees_table.setColumnWidth(1, 300)
        self.employees_table.setColumnWidth(5, 210)
        self.employees_table.setColumnWidth(6, 300)
        self.employees_table.setColumnWidth(7, 300)
        self.employees_table.setColumnWidth(8, 150)
        self.employees_table.setColumnWidth(9, 300)
        self.employees_table.setColumnWidth(10, 150)
        
        self.employees_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.employees_table.setHorizontalHeaderLabels(['ID',
                                                        'ФИО',
                                                        'Серия паспорта',
                                                        'Номер паспорта',
                                                        'Должность',
                                                        'Результаты инструктажа',
                                                        'Инструктаж',
                                                        'Экзамен на допуск',
                                                        'Результаты',
                                                        'Медосмотр',
                                                        'Результаты'])
        self.employees_table.verticalHeader().setVisible(False)
        