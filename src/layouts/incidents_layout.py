from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy, QMessageBox, QDialog)
from PyQt5.QtCore import Qt
import os

from src.dialogs.incidents.insert_incident_dialog import InsertIncidentDialog
from src.dialogs.incidents.search_incident_dialog import SearchIncidentDialog
from src.dialogs.incidents.update_incident_dialog import UpdateIncidentDialog


class IncidentsLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Подключаем существующий экземпляр БД
        self.db = db

        layout = QVBoxLayout()

        # Размещение элементов
        layout.addWidget(QLabel('Список:'))
        self.incidents_layout = QHBoxLayout()
        self.incidents_table = QTableWidget()
        self.incidents_layout.addWidget(self.incidents_table, stretch=6)  # Таблица займет 6/9 пространства
        self.incidents_buttons_layout = QVBoxLayout()
        self.incidents_layout.setSpacing(25)
        self.incidents_search_button = QPushButton('Найти')
        self.incidents_insert_button = QPushButton('Добавить')
        self.incidents_update_button = QPushButton('Изменить')
        self.incidents_delete_button = QPushButton('Удалить')
        self.incidents_reset_button = QPushButton('Обновить')
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

        # Отслеживаем нажатие кнопок
        self.incidents_search_button.clicked.connect(self.incidents_search_button_clicked)
        self.incidents_insert_button.clicked.connect(self.incidents_insert_button_clicked)
        self.incidents_update_button.clicked.connect(self.incidents_update_button_clicked)
        self.incidents_delete_button.clicked.connect(self.incidents_delete_button_clicked)
        self.incidents_reset_button.clicked.connect(self.incidents_reset_button_clicked)

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
            QMessageBox.warning(None, "Файл не найден", "Указанный путь не содержит файла")

    def incidents_search_button_clicked(self):
        dialog = SearchIncidentDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_incidents(search_params)
            self.incidents_table.setRowCount(0)
            if data:
                self.fill_incidents_table(data)

    def incidents_insert_button_clicked(self):
        engineers = self.db.get_engineers()
        employees = self.db.get_employees()
        dialog = InsertIncidentDialog(engineers, employees)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            for engineer in engineers:
                if engineer[1] == data['responsible']:
                    data['responsible'] = engineer[0]
                    break

            if data['participant']:
                for employee in employees:
                    if employee[1] == data['participant']:
                        data['participant'] = employee[0]
                        break

            self.db.insert_incident(data)
            self.incidents_table.setRowCount(0)
            self.fill_incidents_table(self.db.get_incidents())

    def incidents_update_button_clicked(self):
        row = self.incidents_table.currentRow()
        if row != -1:
            to_update = self.incidents_table.item(row, 0).text()
            engineers = self.db.get_engineers()
            employees = self.db.get_employees()
            current = [i if i else '' for i in self.db.get_incident_by_id(to_update)[0]]
            dialog = UpdateIncidentDialog(current, engineers, employees)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                for engineer in engineers:
                    if engineer[1] == data['responsible']:
                        data['responsible'] = engineer[0]
                        break

                if data['participant']:
                    for employee in employees:
                        if employee[1] == data['participant']:
                            data['participant'] = employee[0]
                            break

                self.db.update_incident(data, to_update)
                self.incidents_table.setRowCount(0)
                self.fill_incidents_table(self.db.get_incidents())

    def incidents_delete_button_clicked(self):
        row = self.incidents_table.currentRow()
        if row != -1:
            to_delete = self.incidents_table.item(row, 0).text()
            self.db.delete_from_incidents(to_delete)
            self.incidents_table.removeRow(row)

    def incidents_reset_button_clicked(self):
        self.incidents_table.setRowCount(0)
        self.fill_incidents_table(self.db.get_incidents())
