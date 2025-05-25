import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt


class MedExaminationsLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Список:'))

        # Размещение элементов
        self.med_exams_layout = QHBoxLayout()
        self.med_exams_table = QTableWidget()
        self.med_exams_layout.addWidget(self.med_exams_table, stretch=4)  # Таблица займет 4/7 пространства
        self.med_exams_buttons_layout = QVBoxLayout()
        self.med_exams_layout.setSpacing(25)
        self.med_exams_search_button = QPushButton('Найти')
        self.med_exams_insert_button = QPushButton('Добавить')
        self.med_exams_update_button = QPushButton('Изменить')
        self.med_exams_delete_button = QPushButton('Удалить')
        self.med_exams_reset_button = QPushButton('Сбросить')
        self.med_exams_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.med_exams_insert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.med_exams_update_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.med_exams_delete_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.med_exams_reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.med_exams_buttons_layout.addWidget(QLabel('Действия:'))
        self.med_exams_buttons_layout.addWidget(self.med_exams_search_button)
        self.med_exams_buttons_layout.addWidget(self.med_exams_insert_button)
        self.med_exams_buttons_layout.addWidget(self.med_exams_update_button)
        self.med_exams_buttons_layout.addWidget(self.med_exams_delete_button)
        self.med_exams_buttons_layout.addWidget(self.med_exams_reset_button)
        self.med_exams_buttons_widget = QWidget()
        self.med_exams_buttons_widget.setLayout(self.med_exams_buttons_layout)
        self.med_exams_buttons_widget.setFixedHeight(275)
        self.med_exams_buttons_layout.setContentsMargins(50, 10, 50, 10)
        self.med_exams_layout.addWidget(self.med_exams_buttons_widget, stretch=3)  # Кнопки займут 3/7 пространства
        layout.addLayout(self.med_exams_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

    def fill_med_exams_table(self, data):
        self.med_exams_table.setRowCount(len(data))
        self.med_exams_table.setColumnCount(len(data[0]))
        for i in range(self.med_exams_table.rowCount()):
            for j in range(self.med_exams_table.columnCount()):
                if j == 4:  # Если это столбец со ссылкой
                    btn = QPushButton("Открыть")
                    btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                    btn.clicked.connect(lambda _, path=data[i][j]: self.open_pdf(path))
                    # Размещаем кнопку в ячейке
                    self.med_exams_table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.med_exams_table.setItem(i, j, item)
        self.med_exams_table.setColumnWidth(0, 50)
        self.med_exams_table.setColumnWidth(1, 500)
        self.med_exams_table.setColumnWidth(2, 200)
        self.med_exams_table.setColumnWidth(3, 200)
        self.med_exams_table.setColumnWidth(4, 250)
        self.med_exams_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.med_exams_table.setHorizontalHeaderLabels(['ID',
                                                        'Наименование',
                                                        'Дата проведения',
                                                        'Результаты',
                                                        'Документация'])
        self.med_exams_table.verticalHeader().setVisible(False)

    def open_pdf(self, file_path):
        """Открывает PDF-файл программой по умолчанию"""
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            print(f"Файл не найден: {file_path}")
