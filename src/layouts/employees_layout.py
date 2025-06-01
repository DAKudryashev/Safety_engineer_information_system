from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy, QMessageBox, QDialog)
from PyQt5.QtCore import Qt

from src.dialogs.employees.insert_employee_dialog import InsertEmployeeDialog
from src.dialogs.employees.seacrh_employee_dialog import SearchEmployeeDialog
from src.dialogs.employees.update_employee_dialog import UpdateEmployeeDialog


class EmployeesLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Подключаем существующий экземпляр БД
        self.db = db

        layout = QVBoxLayout()

        # Размещение элементов
        layout.addWidget(QLabel('Список:'))
        self.employees_layout = QHBoxLayout()
        self.employees_table = QTableWidget()
        self.employees_layout.addWidget(self.employees_table, stretch=6)  # Таблица займет 6/9 пространства
        self.employees_buttons_layout = QVBoxLayout()
        self.employees_layout.setSpacing(25)
        self.employees_search_button = QPushButton('Найти')
        self.employees_insert_button = QPushButton('Добавить')
        self.employees_update_button = QPushButton('Изменить')
        self.employees_delete_button = QPushButton('Удалить')
        self.employees_reset_button = QPushButton('Обновить')
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

        # Обрабатываем нажатия кнопок
        self.employees_search_button.clicked.connect(self.employees_search_button_clicked)
        self.employees_insert_button.clicked.connect(self.employees_insert_button_clicked)
        self.employees_update_button.clicked.connect(self.employees_update_button_clicked)
        self.employees_delete_button.clicked.connect(self.employees_delete_button_clicked)
        self.employees_reset_button.clicked.connect(self.employees_reset_button_clicked)
    
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

    def employees_search_button_clicked(self):
        dialog = SearchEmployeeDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_employees(search_params)
            self.employees_table.setRowCount(0)
            if data:
                self.fill_employees_table(data)

    def employees_insert_button_clicked(self):
        briefings = self.db.get_completed_briefings()
        exams = self.db.get_examinations()
        medical_exams = self.db.get_med_examinations()
        dialog = InsertEmployeeDialog(briefings, exams, medical_exams)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            # Ищем соответсвующий ID инструктажа
            if data['briefing'] is not None:
                for briefing in briefings:
                    if briefing[1] == data['briefing']:
                        data['briefing'] = briefing[0]
                        break

            # Ищем соответсвующий ID экзамена
            if data['exam'] is not None:
                for exam in exams:
                    if exam[1] == data['exam']:
                        data['exam'] = exam[0]
                        break

            # Ищем соответсвующий ID медосмотра
            if data['medical_exam'] is not None:
                for exam in medical_exams:
                    if exam[1] == data['medical_exam']:
                        data['medical_exam'] = exam[0]
                        break

            print(data)
            self.db.insert_employee(data)
            self.employees_table.setRowCount(0)
            self.fill_employees_table(self.db.get_employees())

    def employees_update_button_clicked(self):
        row = self.employees_table.currentRow()
        if row != -1:
            # Собираем уже имеющиеся данные и передаем в окно
            to_update = self.employees_table.item(row, 0).text()
            briefings = self.db.get_completed_briefings()
            exams = self.db.get_examinations()
            medical_exams = self.db.get_med_examinations()
            current = []
            for i in range(1, self.employees_table.columnCount()):
                current.append(self.employees_table.item(row, i).text())

            dialog = UpdateEmployeeDialog(current, briefings, exams, medical_exams)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                # Ищем соответсвующий ID инструктажа
                if data['briefing'] is not None:
                    for briefing in briefings:
                        if briefing[1] == data['briefing']:
                            data['briefing'] = briefing[0]
                            break

                # Ищем соответсвующий ID экзамена
                if data['exam'] is not None:
                    for exam in exams:
                        if exam[1] == data['exam']:
                            data['exam'] = exam[0]
                            break

                # Ищем соответсвующий ID медосмотра
                if data['medical_exam'] is not None:
                    for exam in medical_exams:
                        if exam[1] == data['medical_exam']:
                            data['medical_exam'] = exam[0]
                            break

                self.db.update_employee(data, to_update)
                self.employees_table.setRowCount(0)
                self.fill_employees_table(self.db.get_employees())

    def employees_delete_button_clicked(self):
        row = self.employees_table.currentRow()
        if row != -1:
            to_delete = self.employees_table.item(row, 0).text()
            if int(to_delete) not in self.db.get_employees_references():
                self.db.delete_from_employees(to_delete)
                self.employees_table.removeRow(row)
            else:
                QMessageBox.warning(None, "Операция отклонена", "Есть внешние ссылки на удаляемый объект!")

    def employees_reset_button_clicked(self):
        self.employees_table.setRowCount(0)
        self.fill_employees_table(self.db.get_employees())
