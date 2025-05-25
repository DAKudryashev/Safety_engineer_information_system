from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt
import os


class BriefingsLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Запланированные инструктажи:'))

        # Размещение элементов для запланированных инструктажей
        self.planned_layout = QHBoxLayout()
        self.planned_table = QTableWidget()
        self.planned_layout.addWidget(self.planned_table, stretch=6)  # Таблица займет 6/7 пространства
        self.planned_buttons_layout = QVBoxLayout()
        self.planned_search_button = QPushButton('Поиск')
        self.planned_insert_button = QPushButton('Добавить')
        self.planned_update_button = QPushButton('Изменить')
        self.planned_delete_button = QPushButton('Удалить')
        self.planned_reset_button = QPushButton('Сбросить')
        self.planned_buttons_layout.addWidget(QLabel('Действия:'))
        self.planned_buttons_layout.addWidget(self.planned_search_button)
        self.planned_buttons_layout.addWidget(self.planned_insert_button)
        self.planned_buttons_layout.addWidget(self.planned_update_button)
        self.planned_buttons_layout.addWidget(self.planned_delete_button)
        self.planned_buttons_layout.addWidget(self.planned_reset_button)
        self.reg_buttons_widget = QWidget()
        self.reg_buttons_widget.setLayout(self.planned_buttons_layout)
        self.reg_buttons_widget.setFixedHeight(260)
        self.planned_layout.addWidget(self.reg_buttons_widget, stretch=1)  # Кнопки займут 1/7 пространства
        layout.addLayout(self.planned_layout)

        layout.addWidget(QLabel('Проведенные инструктажи:'))

        # Размещение элементов для проведенных инструктажей
        self.completed_layout = QHBoxLayout()
        self.completed_table = QTableWidget()
        self.completed_layout.addWidget(self.completed_table, stretch=6)  # Таблица займет 6/7 пространства
        self.completed_buttons_layout = QVBoxLayout()
        self.comp_search_button = QPushButton('Поиск')
        self.comp_insert_button = QPushButton('Добавить')
        self.comp_update_button = QPushButton('Изменить')
        self.comp_delete_button = QPushButton('Удалить')
        self.comp_reset_button = QPushButton('Сбросить')
        self.completed_buttons_layout.addWidget(QLabel('Действия:'))
        self.completed_buttons_layout.addWidget(self.comp_search_button)
        self.completed_buttons_layout.addWidget(self.comp_insert_button)
        self.completed_buttons_layout.addWidget(self.comp_update_button)
        self.completed_buttons_layout.addWidget(self.comp_delete_button)
        self.completed_buttons_layout.addWidget(self.comp_reset_button)
        self.comp_buttons_widget = QWidget()
        self.comp_buttons_widget.setLayout(self.completed_buttons_layout)
        self.comp_buttons_widget.setFixedHeight(260)
        self.completed_layout.addWidget(self.comp_buttons_widget, stretch=1)  # Кнопки займут 1/7 пространства
        layout.addLayout(self.completed_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

    def fill_planned_table(self, data):
        self.planned_table.setRowCount(len(data))
        self.planned_table.setColumnCount(len(data[0]))
        for i in range(self.planned_table.rowCount()):
            for j in range(self.planned_table.columnCount()):
                if j == 5:  # Если это столбец со ссылкой
                    if data[i][j] is not None:
                        btn = QPushButton("Открыть")
                        btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                        btn.clicked.connect(lambda _, path=data[i][j]: self.open_pdf(path))
                        # Размещаем кнопку в ячейке
                        self.planned_table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.planned_table.setItem(i, j, item)
        self.planned_table.setColumnWidth(0, 50)
        self.planned_table.setColumnWidth(1, 870)
        self.planned_table.setColumnWidth(2, 350)
        self.planned_table.setColumnWidth(3, 200)
        self.planned_table.setColumnWidth(4, 350)
        self.planned_table.setColumnWidth(5, 250)
        self.planned_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.planned_table.setHorizontalHeaderLabels(['ID',
                                                      'Название',
                                                      'Содержание',
                                                      'Дата проведения',
                                                      'Ответственный',
                                                      'Регулирующий документ'])
        self.planned_table.verticalHeader().setVisible(False)

    def fill_completed_table(self, data):
        self.completed_table.setRowCount(len(data))
        self.completed_table.setColumnCount(len(data[0]))
        for i in range(self.completed_table.rowCount()):
            for j in range(self.completed_table.columnCount()):
                if j == 5:  # Если это столбец со ссылкой
                    if data[i][j] is not None:
                        btn = QPushButton("Открыть")
                        btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                        btn.clicked.connect(lambda _, path=data[i][j]: self.open_pdf(path))
                        # Размещаем кнопку в ячейке
                        self.completed_table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.completed_table.setItem(i, j, item)
        self.completed_table.setColumnWidth(0, 50)
        self.completed_table.setColumnWidth(1, 870)
        self.completed_table.setColumnWidth(2, 350)
        self.completed_table.setColumnWidth(3, 200)
        self.completed_table.setColumnWidth(4, 350)
        self.completed_table.setColumnWidth(5, 250)
        self.completed_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.completed_table.setHorizontalHeaderLabels(['ID',
                                                        'Название',
                                                        'Содержание',
                                                        'Дата проведения',
                                                        'Ответственный',
                                                        'Регулирующий документ'])
        self.completed_table.verticalHeader().setVisible(False)

    def open_pdf(self, file_path):
        """Открывает PDF-файл программой по умолчанию"""
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            print(f"Файл не найден: {file_path}")
