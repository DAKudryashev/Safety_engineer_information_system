from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox,
                             QTableWidget, QTableWidgetItem, QPushButton, QDialog)
from PyQt5.QtCore import Qt
import webbrowser
import os

from src.dialogs.documents.insert_regulatory_document_dialog import InsertRegulatoryDialog
from src.dialogs.documents.search_regulatory_document_dialog import SearchRegulatoryDialog
from src.dialogs.documents.update_regulatory_document_dialog import UpdateRegulatoryDialog
from src.dialogs.documents.insert_internal_document_dialog import InsertInternalDialog
from src.dialogs.documents.search_internal_document_dialog import SearchInternalDialog
from src.dialogs.documents.update_internal_document_dialog import UpdateInternalDialog


class DocumentsLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Подключаем существующий экземпляр БД
        self.db = db

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Регулирующие документы:'))

        # Размещение элементов для регулирующий документов
        self.regulatory_layout = QHBoxLayout()
        self.regulatory_table = QTableWidget()
        self.regulatory_layout.addWidget(self.regulatory_table, stretch=6)  # Таблица займет 6/7 пространства
        self.regulatory_buttons_layout = QVBoxLayout()
        self.reg_search_button = QPushButton('Поиск')
        self.reg_insert_button = QPushButton('Добавить')
        self.reg_update_button = QPushButton('Изменить')
        self.reg_delete_button = QPushButton('Удалить')
        self.reg_reset_button = QPushButton('Обновить')
        self.regulatory_buttons_layout.addWidget(QLabel('Действия:'))
        self.regulatory_buttons_layout.addWidget(self.reg_search_button)
        self.regulatory_buttons_layout.addWidget(self.reg_insert_button)
        self.regulatory_buttons_layout.addWidget(self.reg_update_button)
        self.regulatory_buttons_layout.addWidget(self.reg_delete_button)
        self.regulatory_buttons_layout.addWidget(self.reg_reset_button)
        self.reg_buttons_widget = QWidget()
        self.reg_buttons_widget.setLayout(self.regulatory_buttons_layout)
        self.reg_buttons_widget.setFixedHeight(260)
        self.regulatory_layout.addWidget(self.reg_buttons_widget, stretch=1)  # Кнопки займут 1/7 пространства
        layout.addLayout(self.regulatory_layout)

        layout.addWidget(QLabel('Внутренние документы:'))

        # Размещение элементов для внутренних документов
        self.internal_layout = QHBoxLayout()
        self.internal_table = QTableWidget()
        self.internal_layout.addWidget(self.internal_table, stretch=6)  # Таблица займет 6/7 пространства
        self.internal_buttons_layout = QVBoxLayout()
        self.inter_search_button = QPushButton('Поиск')
        self.inter_insert_button = QPushButton('Добавить')
        self.inter_update_button = QPushButton('Изменить')
        self.inter_delete_button = QPushButton('Удалить')
        self.inter_reset_button = QPushButton('Обновить')
        self.internal_buttons_layout.addWidget(QLabel('Действия:'))
        self.internal_buttons_layout.addWidget(self.inter_search_button)
        self.internal_buttons_layout.addWidget(self.inter_insert_button)
        self.internal_buttons_layout.addWidget(self.inter_update_button)
        self.internal_buttons_layout.addWidget(self.inter_delete_button)
        self.internal_buttons_layout.addWidget(self.inter_reset_button)
        self.inter_buttons_widget = QWidget()
        self.inter_buttons_widget.setLayout(self.internal_buttons_layout)
        self.inter_buttons_widget.setFixedHeight(260)
        self.internal_layout.addWidget(self.inter_buttons_widget, stretch=1)  # Кнопки займут 1/7 пространства
        layout.addLayout(self.internal_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

        # Отслеживаем нажатие кнопок
        self.reg_search_button.clicked.connect(self.reg_search_button_clicked)
        self.reg_insert_button.clicked.connect(self.reg_insert_button_clicked)
        self.reg_update_button.clicked.connect(self.reg_update_button_clicked)
        self.reg_delete_button.clicked.connect(self.reg_delete_button_clicked)
        self.reg_reset_button.clicked.connect(self.reg_reset_button_clicked)

        self.inter_search_button.clicked.connect(self.inter_search_button_clicked)
        self.inter_insert_button.clicked.connect(self.inter_insert_button_clicked)
        self.inter_update_button.clicked.connect(self.inter_update_button_clicked)
        self.inter_delete_button.clicked.connect(self.inter_delete_button_clicked)
        self.inter_reset_button.clicked.connect(self.inter_reset_button_clicked)
        
    def fill_regulatory_table(self, data):
        self.regulatory_table.setRowCount(len(data))
        self.regulatory_table.setColumnCount(len(data[0]))
        for i in range(self.regulatory_table.rowCount()):
            for j in range(self.regulatory_table.columnCount()):
                if j == 3:  # Если это столбец со ссылкой
                    btn = QPushButton("Открыть")
                    btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                    btn.clicked.connect(lambda _, url=data[i][j]: webbrowser.open(url))
                    # Размещаем кнопку в ячейке
                    self.regulatory_table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.regulatory_table.setItem(i, j, item)
        self.regulatory_table.setColumnWidth(0, 50)
        self.regulatory_table.setColumnWidth(1, 1500)
        self.regulatory_table.setColumnWidth(3, 300)
        self.regulatory_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.regulatory_table.setHorizontalHeaderLabels(['ID',
                                                         'Название',
                                                         'Дата создания',
                                                         'Посмотреть содержание'])
        self.regulatory_table.verticalHeader().setVisible(False)

    def fill_internal_table(self, data):
        self.internal_table.setRowCount(len(data))
        self.internal_table.setColumnCount(len(data[0]))
        for i in range(self.internal_table.rowCount()):
            for j in range(self.internal_table.columnCount()):
                if j == 4:  # Если это столбец со ссылкой
                    btn = QPushButton("Открыть")
                    btn.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                    btn.clicked.connect(lambda _, path=data[i][j]: self.open_pdf(path))
                    # Размещаем кнопку в ячейке
                    self.internal_table.setCellWidget(i, j, btn)
                else:
                    if j == 0:
                        item = QTableWidgetItem(str(data[i][j]))
                    else:
                        item = QTableWidgetItem(data[i][j])
                    self.internal_table.setItem(i, j, item)
        self.internal_table.setColumnWidth(0, 50)
        self.internal_table.setColumnWidth(1, 1200)
        self.internal_table.setColumnWidth(3, 350)
        self.internal_table.setColumnWidth(4, 250)
        self.internal_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.internal_table.setHorizontalHeaderLabels(['ID',
                                                       'Название',
                                                       'Дата создания',
                                                       'Добавил',
                                                       'Посмотреть содержание'])
        self.internal_table.verticalHeader().setVisible(False)

    def open_pdf(self, file_path):
        """Открывает PDF-файл программой по умолчанию"""
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            QMessageBox.warning(None, "Файл не найден", "Указанный путь не содержит файла")

    def reg_search_button_clicked(self):
        dialog = SearchRegulatoryDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_regulatory_documents(search_params)
            self.regulatory_table.setRowCount(0)
            if data:
                self.fill_regulatory_table(data)

    def reg_insert_button_clicked(self):
        dialog = InsertRegulatoryDialog()
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.db.insert_regulatory_document(data)
            self.regulatory_table.setRowCount(0)
            self.fill_regulatory_table(self.db.get_regulatory_documents())

    def reg_update_button_clicked(self):
        row = self.regulatory_table.currentRow()
        if row != -1:
            to_update = self.regulatory_table.item(row, 0).text()
            current = [i for i in self.db.get_regulatory_document_by_id(to_update)[0]]
            dialog = UpdateRegulatoryDialog(current)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                self.db.update_regulatory_document(data, to_update)
                self.regulatory_table.setRowCount(0)
                self.fill_regulatory_table(self.db.get_regulatory_documents())

    def reg_delete_button_clicked(self):
        row = self.regulatory_table.currentRow()
        if row != -1:
            to_delete = self.regulatory_table.item(row, 0).text()
            self.db.delete_from_regulatory_documents(to_delete)
            self.regulatory_table.removeRow(row)

    def reg_reset_button_clicked(self):
        self.regulatory_table.setRowCount(0)
        self.fill_regulatory_table(self.db.get_regulatory_documents())

    def inter_search_button_clicked(self):
        dialog = SearchInternalDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_internal_documents(search_params)
            self.internal_table.setRowCount(0)
            if data:
                self.fill_internal_table(data)

    def inter_insert_button_clicked(self):
        engineers = self.db.get_engineers_without_passwords()
        dialog = InsertInternalDialog(engineers)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            # Подпираем соответствующий ID добавившего
            for engineer in engineers:
                if data['responsible'] == engineer[1]:
                    data['responsible'] = engineer[0]
                    break

            self.db.insert_internal_document(data)
            self.internal_table.setRowCount(0)
            self.fill_internal_table(self.db.get_internal_documents())

    def inter_update_button_clicked(self):
        row = self.internal_table.currentRow()
        if row != -1:
            # Собираем уже имеющиеся данные и передаем в диалоговое окно
            to_update = self.internal_table.item(row, 0).text()
            engineers = self.db.get_engineers_without_passwords()
            current = [i for i in self.db.get_internal_document_by_id(to_update)[0]]

            dialog = UpdateInternalDialog(current, engineers)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                # Подпираем соответствующий ID добавившего
                for engineer in engineers:
                    if data['responsible'] == engineer[1]:
                        data['responsible'] = engineer[0]
                        break

                self.db.update_internal_document(data, to_update)
                self.internal_table.setRowCount(0)
                self.fill_internal_table(self.db.get_internal_documents())

    def inter_delete_button_clicked(self):
        row = self.internal_table.currentRow()
        if row != -1:
            to_delete = self.internal_table.item(row, 0).text()
            if int(to_delete) not in self.db.get_internal_documents_references():
                self.db.delete_from_internal_documents(to_delete)
                self.internal_table.removeRow(row)
            else:
                QMessageBox.warning(None, "Операция отклонена", "Есть внешние ссылки на удаляемый объект!")

    def inter_reset_button_clicked(self):
        self.internal_table.setRowCount(0)
        self.fill_internal_table(self.db.get_internal_documents())
