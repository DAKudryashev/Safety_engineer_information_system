from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
                             QDateEdit, QPushButton, QLabel)
from PyQt5.QtCore import QDate, Qt


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск записей")
        self.setFixedSize(550, 400)  # Увеличенный размер

        # Стилизация
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

        # Поля для ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Наименование (любая часть)")

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Состояние (любая часть)")

        # Два поля для дат с календарем
        self.date_from = QDateEdit()
        self.date_from.setDisplayFormat("dd.MM.yyyy")
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate(1990, 1, 1))

        self.date_to = QDateEdit()
        self.date_to.setDisplayFormat("dd.MM.yyyy")
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())

        self.responsible_input = QLineEdit()
        self.responsible_input.setPlaceholderText("Ответственный (любая часть)")

        # Надпись об ошибке
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()

        # Кнопки
        self.ok_btn = QPushButton("ОК")
        self.ok_btn.clicked.connect(self.validate_dates)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        # Компоновка
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 10)

        form_layout.addRow("Наименование:", self.name_input)
        form_layout.addRow("Состояние:", self.status_input)
        form_layout.addRow("Дата (с):", self.date_from)
        form_layout.addRow("Дата (по):", self.date_to)
        form_layout.addRow("Ответственный:", self.responsible_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.ok_btn)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.error_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def validate_dates(self):
        """Проверяет заполнение дат"""
        if self.date_from.date() > self.date_to.date():
            self.error_label.setText("Дата 'с' не может быть больше даты 'по'!")
            self.error_label.show()
            return

        self.error_label.hide()
        self.accept()

    def get_search_params(self):
        """Возвращает параметры поиска"""
        return {
            "name": self.name_input.text().strip(),
            "state": self.status_input.text().strip(),
            "date_from": self.date_from.date().toString("yyyy-MM-dd"),
            "date_to": self.date_to.date().toString("yyyy-MM-dd"),
            "responsible": self.responsible_input.text().strip()
        }