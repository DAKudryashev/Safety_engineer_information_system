from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QDateEdit, QPushButton, QLabel, QComboBox)
from PyQt5.QtCore import QDate, Qt


class UpdateEquipmentDialog(QDialog):
    def __init__(self, current, rooms, engineers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Изменить оборудование")
        self.setFixedSize(500, 450)

        # Подготовка данных для ComboBox
        self.rooms = [item[1] for item in rooms]
        self.engineers = [item[1] for item in engineers][1:]

        # Стилизация (сохраняем единый стиль)
        self.setStyleSheet("""
            QDialog {
                background: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLineEdit, QDateEdit, QComboBox {
                padding: 8px;
                border: 1px solid #aaa;
                border-radius: 4px;
                min-width: 200px;
                font-size: 14px;
            }
            QPushButton {
                background: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                min-width: 100px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #45a049;
            }
            QPushButton#cancelButton {
                background: #f44336;
            }
            QPushButton#cancelButton:hover {
                background: #d32f2f;
            }
            #errorLabel {
                color: red;
                font-weight: normal;
                margin-top: 10px;
                margin-bottom: 10px;
            }
        """)

        # Элементы формы
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите наименование оборудования")
        self.name_input.setText(current[0])

        # Выпадающий список с местоположением
        self.room_combo = QComboBox()
        self.room_combo.addItems(self.rooms)
        index = self.room_combo.findText(current[1])
        if self.rooms:
            self.room_combo.setCurrentIndex(index)

        self.supplier_input = QLineEdit()
        self.supplier_input.setPlaceholderText("Введите поставщика")
        self.supplier_input.setText(current[2])

        # Виджеты выбора даты
        self.manufacture_date_edit = QDateEdit()
        self.manufacture_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.manufacture_date_edit.setCalendarPopup(True)
        data = QDate.fromString(current[3], "dd.MM.yyyy")
        self.manufacture_date_edit.setDate(data)

        self.expiry_date_edit = QDateEdit()
        self.expiry_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.expiry_date_edit.setCalendarPopup(True)
        data = QDate.fromString(current[4], "dd.MM.yyyy")
        self.expiry_date_edit.setDate(data)

        # Выпадающий список с ответственными
        self.responsible_combo = QComboBox()
        self.responsible_combo.addItems(self.engineers)
        index = self.responsible_combo.findText(current[5])
        if self.engineers:
            self.responsible_combo.setCurrentIndex(index)
        self.responsible_combo.view().setMinimumWidth(300)

        # Надпись об ошибке
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setText("Заполните все поля!")
        self.error_label.hide()

        # Кнопки
        self.submit_btn = QPushButton("Сохранить")
        self.submit_btn.clicked.connect(self.validate_form)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        # Компоновка
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 10)

        form_layout.addRow("Наименование:", self.name_input)
        form_layout.addRow("Местоположение:", self.room_combo)
        form_layout.addRow("Поставщик:", self.supplier_input)
        form_layout.addRow("Дата изготовления:", self.manufacture_date_edit)
        form_layout.addRow("Годен до:", self.expiry_date_edit)
        form_layout.addRow("Ответственный:", self.responsible_combo)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.submit_btn)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.error_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def validate_form(self):
        """Проверяет заполнение всех обязательных полей"""
        if (not self.name_input.text().strip() or
                not self.supplier_input.text().strip() or
                not (self.rooms and self.room_combo.currentText()) or
                not (self.engineers and self.responsible_combo.currentText())):
            self.error_label.show()
            return

        # Проверка, что дата "годен до" не раньше даты изготовления
        if self.manufacture_date_edit.date() > self.expiry_date_edit.date():
            self.error_label.setText("Дата 'Годен до' не может быть раньше даты изготовления!")
            self.error_label.show()
            return

        self.error_label.hide()
        self.accept()

    def get_data(self):
        """Возвращает введенные данные в структурированном виде"""
        return {
            'name': self.name_input.text().strip(),
            'room': self.room_combo.currentText(),
            'supplier': self.supplier_input.text().strip(),
            'manufacture_date': self.manufacture_date_edit.date().toString("yyyy-MM-dd"),
            'expiry_date': self.expiry_date_edit.date().toString("yyyy-MM-dd"),
            'responsible': self.responsible_combo.currentText()
        }
