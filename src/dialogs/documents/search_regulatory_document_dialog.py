from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QDateEdit, QPushButton, QLabel)
from PyQt5.QtCore import QDate, Qt


class SearchRegulatoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск документов")
        self.setFixedSize(500, 300)

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

        # Элементы формы
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название для поиска")

        # Виджеты выбора даты (от и до)
        self.date_from_edit = QDateEdit()
        self.date_from_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_from_edit.setCalendarPopup(True)
        self.date_from_edit.setDate(QDate(1990, 1, 1))  # По умолчанию месяц назад

        self.date_to_edit = QDateEdit()
        self.date_to_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_to_edit.setCalendarPopup(True)
        self.date_to_edit.setDate(QDate.currentDate())  # По умолчанию текущая дата

        # Надпись об ошибке
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()

        # Кнопки
        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.validate_form)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        # Компоновка
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 10)

        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Дата (с):", self.date_from_edit)
        form_layout.addRow("Дата (по):", self.date_to_edit)

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

    def validate_form(self):
        """Проверяет только корректность диапазона дат"""
        # Проверка, что дата "по" не меньше даты "с"
        if self.date_from_edit.date() > self.date_to_edit.date():
            self.error_label.setText("Дата 'по' не может быть раньше даты 'с'!")
            self.error_label.show()
            return

        self.error_label.hide()
        self.accept()

    def get_search_params(self):
        """Возвращает параметры поиска в виде словаря"""
        return {
            'name': self.name_input.text().strip(),
            'date_from': self.date_from_edit.date().toString("yyyy-MM-dd"),
            'date_to': self.date_to_edit.date().toString("yyyy-MM-dd")
        }
