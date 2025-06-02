import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy, QMessageBox, QDialog)
from PyQt5.QtCore import Qt

from src.dialogs.med_examinations.insert_med_examination_dialog import InsertMedExamDialog
from src.dialogs.med_examinations.search_med_examination_dialog import SearchMedExamDialog
from src.dialogs.med_examinations.update_med_examination_dialog import UpdateMedExamDialog


class MedExaminationsLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Подключаем существующий экземпляр БД
        self.db = db

        layout = QVBoxLayout()

        # Размещение элементов
        layout.addWidget(QLabel('Список:'))
        self.med_exams_layout = QHBoxLayout()
        self.med_exams_table = QTableWidget()
        self.med_exams_layout.addWidget(self.med_exams_table, stretch=4)  # Таблица займет 4/7 пространства
        self.med_exams_buttons_layout = QVBoxLayout()
        self.med_exams_layout.setSpacing(25)
        self.med_exams_search_button = QPushButton('Найти')
        self.med_exams_insert_button = QPushButton('Добавить')
        self.med_exams_update_button = QPushButton('Изменить')
        self.med_exams_delete_button = QPushButton('Удалить')
        self.med_exams_reset_button = QPushButton('Обновить')
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

        # Отслеживаем нажатие на кнопки
        self.med_exams_search_button.clicked.connect(self.med_exams_search_button_clicked)
        self.med_exams_insert_button.clicked.connect(self.med_exams_insert_button_clicked)
        self.med_exams_update_button.clicked.connect(self.med_exams_update_button_clicked)
        self.med_exams_delete_button.clicked.connect(self.med_exams_delete_button_clicked)
        self.med_exams_reset_button.clicked.connect(self.med_exams_reset_button_clicked)

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
            QMessageBox.warning(None, "Файл не найден", "Указанный путь не содержит файла")

    def med_exams_search_button_clicked(self):
        dialog = SearchMedExamDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_med_examinations(search_params)
            self.med_exams_table.setRowCount(0)
            if data:
                self.fill_med_exams_table(data)

    def med_exams_insert_button_clicked(self):
        documents = self.db.get_internal_documents()
        dialog = InsertMedExamDialog(documents)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            # Подбираем соответствующий ID документа
            for document in documents:
                if document[1] == data['document']:
                    data['document'] = document[0]
                    break

            self.db.insert_med_examination(data)
            self.med_exams_table.setRowCount(0)
            self.fill_med_exams_table(self.db.get_med_examinations())

    def med_exams_update_button_clicked(self):
        row = self.med_exams_table.currentRow()
        if row != -1:
            # Собираем уже имеющиеся данные и передаем в диалоговое окно
            to_update = self.med_exams_table.item(row, 0).text()
            current = [i for i in self.db.get_med_examination_by_id(to_update)[0]]
            documents = self.db.get_internal_documents()

            # Находим соответствующий ссылке документ
            for document in documents:
                if current[3] == document[4]:
                    current[3] = document[1]
                    break

            print(current)

            dialog = UpdateMedExamDialog(current, documents)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                # Подбираем соответствующий ID документа
                for document in documents:
                    if document[1] == data['document']:
                        data['document'] = document[0]
                        break

                self.db.update_med_examination(data, to_update)
                self.med_exams_table.setRowCount(0)
                self.fill_med_exams_table(self.db.get_med_examinations())

    def med_exams_delete_button_clicked(self):
        row = self.med_exams_table.currentRow()
        if row != -1:
            to_delete = self.med_exams_table.item(row, 0).text()
            if int(to_delete) not in self.db.get_med_examinations_references():
                self.db.delete_from_med_examinations(to_delete)
                self.med_exams_table.removeRow(row)
            else:
                QMessageBox.warning(None, "Операция отклонена", "Есть внешние ссылки на удаляемый объект!")

    def med_exams_reset_button_clicked(self):
        self.med_exams_table.setRowCount(0)
        self.fill_med_exams_table(self.db.get_med_examinations())
