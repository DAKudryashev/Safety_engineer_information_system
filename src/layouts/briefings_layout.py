from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QPushButton, QDialog)
from PyQt5.QtCore import Qt
import os

from src.dialogs.briefings.insert_planned_briefing_dialog import InsertPlannedDialog
from src.dialogs.briefings.seacrh_planned_briefing_dialog import SearchPlannedDialog
from src.dialogs.briefings.update_planned_briefing_dialog import UpdatePlannedDialog


class BriefingsLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        layout = QVBoxLayout()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Подключаем существующий экземпляр БД
        self.db = db

        # Размещение элементов для запланированных инструктажей
        layout.addWidget(QLabel('Запланированные инструктажи:'))
        self.planned_layout = QHBoxLayout()
        self.planned_table = QTableWidget()
        self.planned_layout.addWidget(self.planned_table, stretch=6)  # Таблица займет 6/7 пространства
        self.planned_buttons_layout = QVBoxLayout()
        self.planned_search_button = QPushButton('Поиск')
        self.planned_insert_button = QPushButton('Добавить')
        self.planned_update_button = QPushButton('Изменить')
        self.planned_delete_button = QPushButton('Удалить')
        self.planned_reset_button = QPushButton('Обновить')
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

        # Размещение элементов для проведенных инструктажей
        layout.addWidget(QLabel('Проведенные инструктажи:'))
        self.completed_layout = QHBoxLayout()
        self.completed_table = QTableWidget()
        self.completed_layout.addWidget(self.completed_table, stretch=6)  # Таблица займет 6/7 пространства
        self.completed_buttons_layout = QVBoxLayout()
        self.comp_search_button = QPushButton('Поиск')
        self.comp_insert_button = QPushButton('Добавить')
        self.comp_update_button = QPushButton('Изменить')
        self.comp_delete_button = QPushButton('Удалить')
        self.comp_reset_button = QPushButton('Обновить')
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

        # Обработка нажатий кнопок запланированного слоя
        self.planned_search_button.clicked.connect(self.planned_search_button_clicked)
        self.planned_insert_button.clicked.connect(self.planned_insert_button_clicked)
        self.planned_update_button.clicked.connect(self.planned_update_button_clicked)
        self.planned_delete_button.clicked.connect(self.planned_delete_button_clicked)
        self.planned_reset_button.clicked.connect(self.planned_reset_button_clicked)

        # Обработка нажатий кнопок проведенного слоя
        self.comp_search_button.clicked.connect(self.completed_search_button_clicked)
        self.comp_insert_button.clicked.connect(self.completed_insert_button_clicked)
        self.comp_update_button.clicked.connect(self.completed_update_button_clicked)
        self.comp_delete_button.clicked.connect(self.completed_delete_button_clicked)
        self.comp_reset_button.clicked.connect(self.completed_reset_button_clicked)

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

    def planned_search_button_clicked(self):
        dialog = SearchPlannedDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_planned_briefings(search_params)
            self.planned_table.setColumnCount(0)
            if data:
                self.fill_planned_table(data)

    def planned_insert_button_clicked(self):
        engineers = self.db.get_engineers_without_passwords()
        documents = self.db.get_internal_documents()
        dialog = InsertPlannedDialog(engineers, documents)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            # Подбираем ID под ФИО ответственного
            for row in engineers:
                if row[1] == data[3]:
                    data[3] = row[0]
                    break

            # Подпираем ID под название документа (при его указании)
            if len(data) == 5:
                for row in documents:
                    if row[1] == data[4]:
                        data[4] = row[0]
                        break

            self.db.insert_planned_briefing(data)
            self.planned_table.setRowCount(0)
            self.fill_planned_table(self.db.get_planned_briefings())

    def planned_update_button_clicked(self):
        row = self.planned_table.currentRow()
        if row != -1:
            # Собираем уже имеющиеся данные и передаем в окно изменения
            to_update = self.planned_table.item(row, 0).text()
            engineers = self.db.get_engineers_without_passwords()
            documents = self.db.get_internal_documents()

            # Извлекаем данные о нынешнем состоянии
            current = [i for i in self.db.get_planned_briefing_by_id(to_update)[0]]
            if current[4]:
                for document in documents:
                    if document[-1] == current[4]:
                        current[4] = document[1]
                        break
            else:
                current[4] = ''

            dialog = UpdatePlannedDialog(current, engineers, documents)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                # Подбираем ID под ФИО ответственного
                for row in engineers:
                    if row[1] == data[3]:
                        data[3] = row[0]
                        break

                # Подпираем ID под название документа (при его указании)
                if len(data) == 5:
                    for row in documents:
                        if row[1] == data[4]:
                            data[4] = row[0]
                            break

                self.db.update_planned_briefing(data, to_update)
                self.planned_table.setRowCount(0)
                self.fill_planned_table(self.db.get_planned_briefings())

    def planned_delete_button_clicked(self):
        row = self.planned_table.currentRow()
        if row != -1:
            self.db.delete_from_planned_briefings(self.planned_table.item(row, 0).text())
            self.planned_table.removeRow(row)

    def planned_reset_button_clicked(self):
        self.planned_table.setColumnCount(0)
        self.fill_planned_table(self.db.get_planned_briefings())

    def completed_search_button_clicked(self):
        pass

    def completed_insert_button_clicked(self):
        pass

    def completed_update_button_clicked(self):
        pass

    def completed_delete_button_clicked(self):
        pass

    def completed_reset_button_clicked(self):
        pass
