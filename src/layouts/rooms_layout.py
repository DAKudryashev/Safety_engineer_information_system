from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy, QMessageBox, QDialog)
from PyQt5.QtCore import Qt

from src.dialogs.rooms.add_room_dialog import AddRowDialog
from src.dialogs.rooms.search_room_dialog import SearchDialog
from src.dialogs.rooms.update_room_dialog import UpdateRoomDialog


class RoomsLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        # Подключаем существующий экземпляр БД
        self.db = db

        layout = QVBoxLayout()

        # Размер шрифта на кнопках
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Размещение элементов
        layout.addWidget(QLabel('Список:'))
        self.rooms_layout = QHBoxLayout()
        self.rooms_table = QTableWidget()
        self.rooms_layout.addWidget(self.rooms_table, stretch=4)  # Таблица займет 4/7 пространства
        self.rooms_buttons_layout = QVBoxLayout()
        self.rooms_layout.setSpacing(25)
        self.rooms_search_button = QPushButton('Найти')
        self.rooms_insert_button = QPushButton('Добавить')
        self.rooms_update_button = QPushButton('Изменить')
        self.rooms_delete_button = QPushButton('Удалить')
        self.rooms_reset_button = QPushButton('Сбросить')
        self.rooms_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_insert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_update_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_delete_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.rooms_buttons_layout.addWidget(QLabel('Действия:'))
        self.rooms_buttons_layout.addWidget(self.rooms_search_button)
        self.rooms_buttons_layout.addWidget(self.rooms_insert_button)
        self.rooms_buttons_layout.addWidget(self.rooms_update_button)
        self.rooms_buttons_layout.addWidget(self.rooms_delete_button)
        self.rooms_buttons_layout.addWidget(self.rooms_reset_button)
        self.rooms_buttons_widget = QWidget()
        self.rooms_buttons_widget.setLayout(self.rooms_buttons_layout)
        self.rooms_buttons_widget.setFixedHeight(275)
        self.rooms_buttons_layout.setContentsMargins(50, 10, 50, 10)
        self.rooms_layout.addWidget(self.rooms_buttons_widget, stretch=3)  # Кнопки займут 3/7 пространства
        layout.addLayout(self.rooms_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

        # Отслеживаем нажатие кнопок
        self.rooms_search_button.clicked.connect(self.search_button_clicked)
        self.rooms_insert_button.clicked.connect(self.insert_button_clicked)
        self.rooms_update_button.clicked.connect(self.update_button_clicked)
        self.rooms_delete_button.clicked.connect(self.rooms_delete_button_clicked)
        self.rooms_reset_button.clicked.connect(self.reset_button_clicked)
    
    def fill_rooms_table(self, data):
        self.rooms_table.setRowCount(len(data))
        self.rooms_table.setColumnCount(len(data[0]))
        for i in range(self.rooms_table.rowCount()):
            for j in range(self.rooms_table.columnCount()):
                item = QTableWidgetItem(str(data[i][j]))
                self.rooms_table.setItem(i, j, item)
        self.rooms_table.setColumnWidth(0, 80)
        self.rooms_table.setColumnWidth(1, 150)
        self.rooms_table.setColumnWidth(2, 300)
        self.rooms_table.setColumnWidth(3, 250)
        self.rooms_table.setColumnWidth(4, 500)
        self.rooms_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.rooms_table.setHorizontalHeaderLabels(['ID',
                                                    'Наименование',
                                                    'Состояние',
                                                    'Дата последней проверки',
                                                    'Ответственный'])
        self.rooms_table.verticalHeader().setVisible(False)

    def search_button_clicked(self):
        dialog = SearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_rooms(search_params)
            self.rooms_table.setRowCount(0)
            if data:
                self.fill_rooms_table(data)

    def insert_button_clicked(self):
        engineers = self.db.get_engineers_without_passwords()
        dialog = AddRowDialog(engineers)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            # Подбираем ID согласно выбранному ФИО
            for row in engineers:
                if row[1] == data[3]:
                    data[3] = row[0]
                    break

            # Обновляем таблицу и отправляем в БД
            self.db.insert_room(data)
            self.rooms_table.setRowCount(0)
            self.fill_rooms_table(self.db.get_rooms())

            QMessageBox.information(self, "Успех", "Запись успешно добавлена!")

    def update_button_clicked(self):
        # Считываем id выбранного элемента
        row = self.rooms_table.currentRow()
        if row != -1:
            # Собираем уже имеющиеся данные и передаем в окно изменения
            to_update = self.rooms_table.item(row, 0).text()
            engineers = self.db.get_engineers_without_passwords()
            current = []
            for i in range(1, self.rooms_table.columnCount()):
                current.append(self.rooms_table.item(row, i).text())
            dialog = UpdateRoomDialog(current, engineers)

            # Обрабатываем положительное завершение диалога
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                # Подбираем ID согласно выбранному ФИО
                for engineer in engineers:
                    if engineer[1] == data[3]:
                        data[3] = engineer[0]
                        break

                # Посылаем в БД и обновляем таблицу
                self.db.update_room(to_update, data)
                self.rooms_table.setRowCount(0)
                self.fill_rooms_table(self.db.get_rooms())

    def rooms_delete_button_clicked(self):
        row = self.rooms_table.currentRow()
        if row != -1:
            to_delete = self.rooms_table.item(row, 0).text()
            # Проверяем наличие внешних ссылок
            if int(to_delete) not in self.db.get_rooms_references():
                self.db.delete_from_rooms(to_delete)
                self.rooms_table.removeRow(row)
            else:
                QMessageBox.warning(None, "Операция отклонена", "Есть внешние ссылки на удаляемый объект!")

    def reset_button_clicked(self):
        self.rooms_table.setRowCount(0)
        self.fill_rooms_table(self.db.get_rooms())
