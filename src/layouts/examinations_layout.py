import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy, QMessageBox, QDialog)
from PyQt5.QtCore import Qt

from src.dialogs.examinations.insert_examination_dialog import InsertExamDialog
from src.dialogs.examinations.search_examination_dialog import SearchExamDialog
from src.dialogs.examinations.update_examination_dialog import UpdateExamDialog


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
        self.exams_reset_button = QPushButton('Обновить')
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

        # Отслеживаем нажатие кнопок
        self.exams_search_button.clicked.connect(self.exams_search_button_clicked)
        self.exams_insert_button.clicked.connect(self.exams_insert_button_clicked)
        self.exams_update_button.clicked.connect(self.exams_update_button_clicked)
        self.exams_delete_button.clicked.connect(self.exams_delete_button_clicked)
        self.exams_reset_button.clicked.connect(self.exams_reset_button_clicked)
        
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
            QMessageBox.warning(None, "Файл не найден", "Указанный путь не содержит файла")

    def exams_search_button_clicked(self):
        dialog = SearchExamDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_examinations(search_params)
            self.exams_table.setRowCount(0)
            if data:
                self.fill_exams_table(data)

    def exams_insert_button_clicked(self):
        engineers = self.db.get_engineers_without_passwords()
        documents = self.db.get_internal_documents()
        dialog = InsertExamDialog(engineers, documents)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            # Подбираем соответствующий ID документа
            for document in documents:
                if document[1] == data['document']:
                    data['document'] = document[0]
                    break

            # Подбираем соответствующий ID инженера
            for engineer in engineers:
                if engineer[1] == data['responsible']:
                    data['responsible'] = engineer[0]
                    break

            self.db.insert_examination(data)
            self.exams_table.setRowCount(0)
            self.fill_exams_table(self.db.get_examinations())

    def exams_update_button_clicked(self):
        row = self.exams_table.currentRow()
        if row != -1:
            # Собираем уже имеющиеся данные и передаем в диалоговое окно
            to_update = self.exams_table.item(row, 0).text()
            current = [i for i in self.db.get_examination_by_id(to_update)[0]]
            engineers = self.db.get_engineers_without_passwords()
            documents = self.db.get_internal_documents()

            # Находим соответствующий ссылке документ
            for document in documents:
                if current[4] == document[4]:
                    current[4] = document[1]
                    break

            dialog = UpdateExamDialog(current, engineers, documents)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                # Подбираем соответствующий ID документа
                for document in documents:
                    if document[1] == data['document']:
                        data['document'] = document[0]
                        break

                # Подбираем соответствующий ID инженера
                for engineer in engineers:
                    if engineer[1] == data['responsible']:
                        data['responsible'] = engineer[0]
                        break

                self.db.update_examination(data, to_update)
                self.exams_table.setRowCount(0)
                self.fill_exams_table(self.db.get_examinations())

    def exams_delete_button_clicked(self):
        row = self.exams_table.currentRow()
        if row != -1:
            to_delete = self.exams_table.item(row, 0).text()
            if int(to_delete) not in self.db.get_examinations_references():
                self.db.delete_from_examinations(to_delete)
                self.exams_table.removeRow(row)
            else:
                QMessageBox.warning(None, "Операция отклонена", "Есть внешние ссылки на удаляемый объект!")

    def exams_reset_button_clicked(self):
        self.exams_table.setRowCount(0)
        self.fill_exams_table(self.db.get_examinations())
