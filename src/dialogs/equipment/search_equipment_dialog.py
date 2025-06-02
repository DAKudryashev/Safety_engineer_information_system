from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QDateEdit, QPushButton, QLabel)
from PyQt5.QtCore import QDate, Qt


class SearchEquipmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск оборудования")
        self.setFixedSize(550, 550)

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
            QLineEdit, QDateEdit {
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
        self.name_input.setPlaceholderText("Введите слово или часть")

        self.room_input = QLineEdit()
        self.room_input.setPlaceholderText("Введите слово или часть")

        self.supplier_input = QLineEdit()
        self.supplier_input.setPlaceholderText("Введите слово или часть")

        # Диапазон дат изготовления
        self.manufacture_from_edit = QDateEdit()
        self.manufacture_from_edit.setDisplayFormat("dd.MM.yyyy")
        self.manufacture_from_edit.setCalendarPopup(True)
        self.manufacture_from_edit.setDate(QDate(1990, 1, 1))

        self.manufacture_to_edit = QDateEdit()
        self.manufacture_to_edit.setDisplayFormat("dd.MM.yyyy")
        self.manufacture_to_edit.setCalendarPopup(True)
        self.manufacture_to_edit.setDate(QDate.currentDate())

        # Диапазон дат годности
        self.expiry_from_edit = QDateEdit()
        self.expiry_from_edit.setDisplayFormat("dd.MM.yyyy")
        self.expiry_from_edit.setCalendarPopup(True)
        self.expiry_from_edit.setDate(QDate.currentDate())

        self.expiry_to_edit = QDateEdit()
        self.expiry_to_edit.setDisplayFormat("dd.MM.yyyy")
        self.expiry_to_edit.setCalendarPopup(True)
        self.expiry_to_edit.setDate(QDate.currentDate().addYears(10))

        self.responsible_input = QLineEdit()
        self.responsible_input.setPlaceholderText("Введите слово или часть")

        # Надпись об ошибке
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()

        # Кнопки
        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.validate_dates)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        # Компоновка
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(20, 20, 20, 10)

        form_layout.addRow("Наименование:", self.name_input)
        form_layout.addRow("Помещение:", self.room_input)
        form_layout.addRow("Поставщик:", self.supplier_input)
        form_layout.addRow("Дата изготовления (с):", self.manufacture_from_edit)
        form_layout.addRow("Дата изготовления (по):", self.manufacture_to_edit)
        form_layout.addRow("Годен до (с):", self.expiry_from_edit)
        form_layout.addRow("Годен до (по):", self.expiry_to_edit)
        form_layout.addRow("Ответственный:", self.responsible_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.search_btn)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.error_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def validate_dates(self):
        """Проверяет корректность диапазонов дат"""
        errors = []

        if self.manufacture_from_edit.date() > self.manufacture_to_edit.date():
            errors.append("Дата изготовления (по) раньше (с)")

        if self.expiry_from_edit.date() > self.expiry_to_edit.date():
            errors.append("Дата годности (по) раньше (с)")

        if errors:
            self.error_label.setText("" + ", ".join(errors))
            self.error_label.show()
        else:
            self.error_label.hide()
            self.accept()

    def get_search_params(self):
        """Возвращает параметры поиска в виде словаря"""
        return {
            'equipment_name': self.name_input.text().strip(),
            'room': self.room_input.text().strip(),
            'supplier': self.supplier_input.text().strip(),
            'manufacture_from': self.manufacture_from_edit.date().toString("yyyy-MM-dd"),
            'manufacture_to': self.manufacture_to_edit.date().toString("yyyy-MM-dd"),
            'expiry_from': self.expiry_from_edit.date().toString("yyyy-MM-dd"),
            'expiry_to': self.expiry_to_edit.date().toString("yyyy-MM-dd"),
            'responsible': self.responsible_input.text().strip()
        }