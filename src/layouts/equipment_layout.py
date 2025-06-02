from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget,
                             QPushButton, QTableWidgetItem, QSizePolicy, QDialog)
from PyQt5.QtCore import Qt

from src.dialogs.equipment.insert_equipment_dialog import InsertEquipmentDialog
from src.dialogs.equipment.search_equipment_dialog import SearchEquipmentDialog
from src.dialogs.equipment.update_equipment_dialog import UpdateEquipmentDialog


class EquipmentLayout(QWidget):
    def __init__(self, db):
        super().__init__()

        # Увеличиваем кнопки
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

        # Подключаем существующий экземпляр БД
        self.db = db

        layout = QVBoxLayout()

        # Размещение элементов
        layout.addWidget(QLabel('Список:'))
        self.equipment_layout = QHBoxLayout()
        self.equipment_table = QTableWidget()
        self.equipment_layout.addWidget(self.equipment_table, stretch=6)  # Таблица займет 6/9 пространства
        self.equipment_buttons_layout = QVBoxLayout()
        self.equipment_layout.setSpacing(25)
        self.equipment_search_button = QPushButton('Найти')
        self.equipment_insert_button = QPushButton('Добавить')
        self.equipment_update_button = QPushButton('Изменить')
        self.equipment_delete_button = QPushButton('Удалить')
        self.equipment_reset_button = QPushButton('Обновить')
        self.equipment_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_insert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_update_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_delete_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_reset_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.equipment_buttons_layout.addWidget(QLabel('Действия:'))
        self.equipment_buttons_layout.addWidget(self.equipment_search_button)
        self.equipment_buttons_layout.addWidget(self.equipment_insert_button)
        self.equipment_buttons_layout.addWidget(self.equipment_update_button)
        self.equipment_buttons_layout.addWidget(self.equipment_delete_button)
        self.equipment_buttons_layout.addWidget(self.equipment_reset_button)
        self.equipment_buttons_widget = QWidget()
        self.equipment_buttons_widget.setLayout(self.equipment_buttons_layout)
        self.equipment_buttons_widget.setFixedHeight(275)
        self.equipment_buttons_layout.setContentsMargins(50, 10, 50, 10)
        self.equipment_layout.addWidget(self.equipment_buttons_widget, stretch=3)  # Кнопки займут 3/9 пространства
        layout.addLayout(self.equipment_layout)

        # Закрепление слоя на вкладке
        self.setLayout(layout)

        # Обрабатываем нажатия кнопок
        self.equipment_search_button.clicked.connect(self.equipment_search_button_clicked)
        self.equipment_insert_button.clicked.connect(self.equipment_insert_button_clicked)
        self.equipment_update_button.clicked.connect(self.equipment_update_button_clicked)
        self.equipment_delete_button.clicked.connect(self.equipment_delete_button_clicked)
        self.equipment_reset_button.clicked.connect(self.equipment_reset_button_clicked)

    def fill_equipment_table(self, data):
        self.equipment_table.setRowCount(len(data))
        self.equipment_table.setColumnCount(len(data[0]))
        for i in range(self.equipment_table.rowCount()):
            for j in range(self.equipment_table.columnCount()):
                item = QTableWidgetItem(str(data[i][j]))
                self.equipment_table.setItem(i, j, item)
        self.equipment_table.setColumnWidth(0, 50)
        self.equipment_table.setColumnWidth(1, 200)
        self.equipment_table.setColumnWidth(2, 200)
        self.equipment_table.setColumnWidth(3, 400)
        self.equipment_table.setColumnWidth(4, 200)
        self.equipment_table.setColumnWidth(6, 350)
        self.equipment_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Вертикальный scrollbar всегда виден
        self.equipment_table.setHorizontalHeaderLabels(['ID',
                                                        'Наименование',
                                                        'Местоположение',
                                                        'Поставщик',
                                                        'Дата изготовления',
                                                        'Годен до',
                                                        'Ответственный'])
        self.equipment_table.verticalHeader().setVisible(False)

    def equipment_search_button_clicked(self):
        dialog = SearchEquipmentDialog()
        if dialog.exec_() == QDialog.Accepted:
            search_params = dialog.get_search_params()
            data = self.db.search_equipment(search_params)
            self.equipment_table.setRowCount(0)
            if data:
                self.fill_equipment_table(data)

    def equipment_insert_button_clicked(self):
        rooms = self.db.get_rooms()
        engineers = self.db.get_engineers()
        dialog = InsertEquipmentDialog(rooms, engineers)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            # Подбираем ID соответствующий помещению
            for room in rooms:
                if room[1] == data['room']:
                    data['room'] = room[0]
                    break

            # Подбираем ID соответствующий инженеру
            for engineer in engineers:
                if engineer[1] == data['responsible']:
                    data['responsible'] = engineer[0]
                    break

            print(data)
            self.db.insert_equipment(data)
            self.equipment_table.setRowCount(0)
            self.fill_equipment_table(self.db.get_equipment())

    def equipment_update_button_clicked(self):
        row = self.equipment_table.currentRow()
        if row != -1:
            # Собираем уже имеющиеся данные и передаем в диалоговое окно
            to_update = self.equipment_table.item(row, 0).text()
            current = [i for i in self.db.get_equipment_by_id(to_update)[0]]
            rooms = self.db.get_rooms()
            engineers = self.db.get_engineers()
            dialog = UpdateEquipmentDialog(current, rooms, engineers)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                # Подбираем ID соответствующий помещению
                for room in rooms:
                    if room[1] == data['room']:
                        data['room'] = room[0]
                        break

                # Подбираем ID соответствующий инженеру
                for engineer in engineers:
                    if engineer[1] == data['responsible']:
                        data['responsible'] = engineer[0]
                        break

                self.db.update_equipment(data, to_update)
                self.equipment_table.setRowCount(0)
                self.fill_equipment_table(self.db.get_equipment())

    def equipment_delete_button_clicked(self):
        row = self.equipment_table.currentRow()
        if row != -1:
            to_delete = self.equipment_table.item(row, 0).text()
            self.db.delete_from_equipment(to_delete)
            self.equipment_table.removeRow(row)

    def equipment_reset_button_clicked(self):
        self.equipment_table.setRowCount(0)
        self.fill_equipment_table(self.db.get_equipment())
