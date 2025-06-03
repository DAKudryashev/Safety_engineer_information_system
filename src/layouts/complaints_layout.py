from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy, QDialog)
from PyQt5.QtCore import Qt

from src.dialogs.complaints.insert_complaint_dialog import InsertComplaintDialog
from src.dialogs.complaints.seacrh_complaint_dialog import SearchComplaintDialog
from src.dialogs.complaints.update_complaint_dialog import UpdateComplaintDialog


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
        self.complaints_reset_button = QPushButton('Обновить')
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

        # Обрабатываем нажатие кнопок
        self.complaints_search_button.clicked.connect(self.complaints_search_button_clicked)
        self.complaints_insert_button.clicked.connect(self.complaints_insert_button_clicked)
        self.complaints_update_button.clicked.connect(self.complaints_update_button_clicked)
        self.complaints_delete_button.clicked.connect(self.complaints_delete_button_clicked)
        self.complaints_reset_button.clicked.connect(self.complaints_reset_button_clicked)

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

    def complaints_search_button_clicked(self):
        dialog = SearchComplaintDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            print(search_params)
            data = self.db.search_complaints(search_params)
            self.complaints_table.setRowCount(0)
            if data:
                self.fill_complaints_table(data)

    def complaints_insert_button_clicked(self):
        engineers = self.db.get_engineers()
        employees = self.db.get_employees()
        dialog = InsertComplaintDialog(employees, engineers)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            for engineer in engineers:
                if engineer[1] == data['responsible']:
                    data['responsible'] = engineer[0]
                    break

            if data['author']:
                for employee in employees:
                    if employee[1] == data['author']:
                        data['author'] = employee[0]
                        break

            self.db.insert_complaint(data)
            self.complaints_table.setRowCount(0)
            self.fill_complaints_table(self.db.get_complaints())

    def complaints_update_button_clicked(self):
        row = self.complaints_table.currentRow()
        if row != -1:
            to_update = self.complaints_table.item(row, 0).text()
            current = [i for i in self.db.get_complaint_by_id(to_update)[0]]
            engineers = self.db.get_engineers()
            employees = self.db.get_employees()
            dialog = UpdateComplaintDialog(current, employees, engineers)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                print(data)

                for engineer in engineers:
                    if engineer[1] == data['responsible']:
                        data['responsible'] = engineer[0]
                        break

                if data['author']:
                    for employee in employees:
                        if employee[1] == data['author']:
                            data['author'] = employee[0]
                            break

                self.db.update_complaint(data, to_update)
                self.complaints_table.setRowCount(0)
                self.fill_complaints_table(self.db.get_complaints())

    def complaints_delete_button_clicked(self):
        row = self.complaints_table.currentRow()
        if row != -1:
            to_delete = self.complaints_table.item(row, 0).text()
            self.db.delete_from_complaints(to_delete)
            self.complaints_table.removeRow(row)

    def complaints_reset_button_clicked(self):
        self.complaints_table.setRowCount(0)
        self.fill_complaints_table(self.db.get_complaints())
