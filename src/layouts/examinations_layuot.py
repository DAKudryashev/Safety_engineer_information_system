import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt


class ExaminationsLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Подключаем существующий экземпляр БД
        self.db = db

        layout = QVBoxLayout()

        # Размещение элементов
        layout.addWidget(QLabel('Список:'))
        self.exams_layout = QHBoxLayout()
        self.exams_table = QTableWidget()
        self.exams_layout.addWidget(self.exams_table, stretch=6)  # Таблица займет 6/9 пространства
        self.exams_buttons_layout = QVBoxLayout()
        self.exams_layout.setSpacing(25)
        self.exams_search_button = QPushButton('Найти')
        self.exams_insert_button = QPushButton('Добавить')
        self.exams_update_button = QPushButton('Изменить')
        self.exams_delete_button = QPushButton('Удалить')
        self.exams_reset_button = QPushButton('Сбросить')
        self.exams_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.exams_insert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.exams_update_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.exams_delete_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.exams_reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.exams_buttons_layout.addWidget(QLabel('Действия:'))
        self.exams_buttons_layout.addWidget(self.exams_search_button)
        self.exams_buttons_layout.addWidget(self.exams_insert_button)
        self.exams_buttons_layout.addWidget(self.exams_update_button)
        self.exams_buttons_layout.addWidget(self.exams_delete_button)
        self.exams_buttons_layout.addWidget(self.exams_reset_button)
        self.exams_buttons_widget = QWidget()
        self.exams_buttons_widget.setLayout(self.exams_buttons_layout)
        self.exams_buttons_widget.setFixedHeight(275)
        self.exams_buttons_layout.setContentsMargins(50, 10, 50, 10)
        self.exams_layout.addWidget(self.exams_buttons_widget, stretch=3)  # Кнопки займут 3/7 пространства
        layout.addLayout(self.exams_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)
        
    def fill_exams_table(self, data):
        self.exams_table.setRowCount(len(data))
        self.exams_table.setColumnCount(len(data[0]))
        for i in range(self.exams_table.rowCount()):
            for j in range(self.exams_table.columnCount()):
                if j == 5:  # Если это столбец со ссылкой
                    btn = QPushButton("Открыть")
                    btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                    btn.clicked.connect(lambda _, path=data[i][j]: self.open_pdf(path))
                    # Размещаем кнопку в ячейке
                    self.exams_table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.exams_table.setItem(i, j, item)
        self.exams_table.setColumnWidth(0, 50)
        self.exams_table.setColumnWidth(1, 500)
        self.exams_table.setColumnWidth(2, 200)
        self.exams_table.setColumnWidth(3, 350)
        self.exams_table.setColumnWidth(5, 250)
        self.exams_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.exams_table.setHorizontalHeaderLabels(['ID',
                                                    'Наименование',
                                                    'Дата проведения',
                                                    'Ответственный',
                                                    'Результаты',
                                                    'Документация'])
        self.exams_table.verticalHeader().setVisible(False)

    def open_pdf(self, file_path):
        """Открывает PDF-файл программой по умолчанию"""
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            print(f"Файл не найден: {file_path}")
