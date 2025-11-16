from PyQt5.QtWidgets import (QWidget, QLabel, QMessageBox, QTableWidgetItem, QPushButton, QDialog)
from PyQt5.QtCore import Qt

from src.dialogs.briefings.insert_planned_briefing_dialog import InsertPlannedDialog
from src.dialogs.briefings.seacrh_planned_briefing_dialog import SearchPlannedDialog
from src.dialogs.briefings.update_planned_briefing_dialog import UpdatePlannedDialog
from src.dialogs.briefings.search_completed_briefing_dialog import SearchCompletedDialog
from src.dialogs.briefings.insert_completed_briefing_dialog import InsertCompletedDialog
from src.dialogs.briefings.update_completed_briefing_dialog import UpdateCompletedDialog
from main_window_tabs.base_layout import BaseLayout
from database import DataBase
from utils import open_document, buttons


class PlannedBriefingsLayout(BaseLayout):
    def __init__(self, db: DataBase):
        super().__init__(db)

    def setup_table(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                if j == 5:  # Если это столбец со ссылкой
                    if data[i][j] is not None:
                        btn = QPushButton("Открыть")
                        btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                        btn.clicked.connect(lambda _, path=data[i][j]: open_document(path))

                        # Размещаем кнопку в ячейке
                        self.table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.table.setItem(i, j, item)

        # Донастройка визуала таблицы
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 870)
        self.table.setColumnWidth(2, 350)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 350)
        self.table.setColumnWidth(5, 250)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Содержание', 'Дата проведения',
                                              'Ответственный', 'Регулирующий документ'])
        self.table.verticalHeader().setVisible(False)

    def setup_buttons_layout(self):
        self.buttons_layout.addWidget(QLabel('Действия:'))
        for text in buttons:
            btn = QPushButton(text)
            self.buttons_layout.addWidget(btn)

            if text == 'Найти':
                btn.clicked.connect(self.search_button_clicked)
            elif text == 'Добавить':
                btn.clicked.connect(self.insert_button_clicked)
            elif text == 'Изменить':
                btn.clicked.connect(self.update_button_clicked)
            elif text == 'Удалить':
                btn.clicked.connect(self.delete_button_clicked)
            elif text == 'Обновить':
                btn.clicked.connect(self.reset_button_clicked)
            else:
                raise Exception('Какой-то кнопке не назначен сигнал!')

    def setup_ui(self):
        self.addWidget(self.table, stretch=6)  # Таблица займет 6/7 пространства

        # Вертикальный layout с кнопками запихиваем в QWidget для регулировки размера
        reg_buttons_widget = QWidget()
        reg_buttons_widget.setLayout(self.buttons_layout)
        reg_buttons_widget.setFixedHeight(260)
        self.addWidget(reg_buttons_widget, stretch=1)  # Кнопки займут 1/7 пространства

    def search_button_clicked(self):
        dialog = SearchPlannedDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_planned_briefings(search_params)
            self.table.setColumnCount(0)
            if data:
                self.setup_table(data)

    def insert_button_clicked(self):
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

            # Подбираем ID под название документа (при его указании)
            if len(data) == 5:
                for row in documents:
                    if row[1] == data[4]:
                        data[4] = row[0]
                        break

            self.db.insert_planned_briefing(data)
            self.table.setRowCount(0)
            self.setup_table(self.db.get_planned_briefings())

    def update_button_clicked(self):
        row = self.table.currentRow()
        if row != -1:
            # Собираем уже имеющиеся данные и передаем в окно изменения
            to_update = self.table.item(row, 0).text()
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

                # Подбираем ID под название документа (при его указании)
                if len(data) == 5:
                    for row in documents:
                        if row[1] == data[4]:
                            data[4] = row[0]
                            break

                self.db.update_planned_briefing(data, to_update)
                self.table.setRowCount(0)
                self.setup_table(self.db.get_planned_briefings())

    def delete_button_clicked(self):
        row = self.table.currentRow()
        if row != -1:
            self.db.delete_from_planned_briefings(self.table.item(row, 0).text())
            self.table.removeRow(row)

    def reset_button_clicked(self):
        self.table.setColumnCount(0)
        self.setup_table(self.db.get_planned_briefings())


class CompletedBriefingsLayout(BaseLayout):
    def __init__(self, db: DataBase):
        super().__init__(db)

    def setup_table(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                if j == 5:  # Если это столбец со ссылкой
                    if data[i][j] is not None:
                        btn = QPushButton("Открыть")
                        btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                        btn.clicked.connect(lambda _, path=data[i][j]: open_document(path))
                        # Размещаем кнопку в ячейке
                        self.table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.table.setItem(i, j, item)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 870)
        self.table.setColumnWidth(2, 350)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 350)
        self.table.setColumnWidth(5, 250)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Содержание', 'Дата проведения', 'Ответственный',
                                              'Регулирующий документ'])
        self.table.verticalHeader().setVisible(False)

    def setup_buttons_layout(self):
        self.buttons_layout.addWidget(QLabel('Действия:'))
        for text in buttons:
            btn = QPushButton(text)
            self.buttons_layout.addWidget(btn)

            if text == 'Найти':
                btn.clicked.connect(self.search_button_clicked)
            elif text == 'Добавить':
                btn.clicked.connect(self.insert_button_clicked)
            elif text == 'Изменить':
                btn.clicked.connect(self.update_button_clicked)
            elif text == 'Удалить':
                btn.clicked.connect(self.delete_button_clicked)
            elif text == 'Обновить':
                btn.clicked.connect(self.reset_button_clicked)
            else:
                raise Exception('Какой-то кнопке не назначен сигнал!')

    def setup_ui(self):
        # Размещение элементов для проведенных инструктажей
        self.addWidget(self.table, stretch=6)  # Таблица займет 6/7 пространства

        comp_buttons_widget = QWidget()
        comp_buttons_widget.setLayout(self.buttons_layout)
        comp_buttons_widget.setFixedHeight(260)
        self.addWidget(comp_buttons_widget, stretch=1)  # Кнопки займут 1/7 пространства


    def search_button_clicked(self):
        dialog = SearchCompletedDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_completed_briefings(search_params)
            self.table.setRowCount(0)
            if data:
                self.setup_table(data)

    def insert_button_clicked(self):
        engineers = self.db.get_engineers_without_passwords()
        documents = self.db.get_internal_documents()
        dialog = InsertCompletedDialog(engineers, documents)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            # Подбираем ID под ФИО ответственного
            for row in engineers:
                if row[1] == data[3]:
                    data[3] = row[0]
                    break

            # Подбираем ID под название документа (при его указании)
            if len(data) == 5:
                for row in documents:
                    if row[1] == data[4]:
                        data[4] = row[0]
                        break

            self.db.insert_completed_briefing(data)
            self.table.setRowCount(0)
            self.setup_table(self.db.get_completed_briefings())

    def update_button_clicked(self):
        row = self.table.currentRow()
        if row != -1:
            # Собираем уже имеющиеся данные и передаем в окно изменения
            to_update = self.table.item(row, 0).text()
            engineers = self.db.get_engineers_without_passwords()
            documents = self.db.get_internal_documents()

            # Извлекаем данные о нынешнем состоянии
            current = [i for i in self.db.get_completed_briefing_by_id(to_update)[0]]
            if current[4]:
                for document in documents:
                    if document[-1] == current[4]:
                        current[4] = document[1]
                        break
            else:
                current[4] = ''

            dialog = UpdateCompletedDialog(current, engineers, documents)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                # Подбираем ID под ФИО ответственного
                for row in engineers:
                    if row[1] == data[3]:
                        data[3] = row[0]
                        break

                # Подбираем ID под название документа (при его указании)
                if len(data) == 5:
                    for row in documents:
                        if row[1] == data[4]:
                            data[4] = row[0]
                            break

                self.db.update_completed_briefing(data, to_update)
                self.table.setRowCount(0)
                self.setup_table(self.db.get_completed_briefings())

    def delete_button_clicked(self):
        row = self.table.currentRow()
        if row != -1:
            to_delete = self.table.item(row, 0).text()
            if int(to_delete) not in self.db.get_completed_briefings_references():
                self.db.delete_from_completed_briefings(to_delete)
                self.table.removeRow(row)
            else:
                QMessageBox.warning(None, "Операция отклонена", "Есть внешние ссылки на удаляемый объект!")

    def reset_button_clicked(self):
        self.table.setRowCount(0)
        self.setup_table(self.db.get_completed_briefings())
