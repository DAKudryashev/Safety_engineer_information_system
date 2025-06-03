from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QDateEdit, QPushButton)
from PyQt5.QtCore import QDate


class SearchComplaintDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск жалоб")
        self.setFixedSize(600, 400)

        # Стилизация (сохранена единая стилистика)
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
                min-width: 250px;
                font-size: 14px;
            }
            QPushButton {
                background: #2196F3;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                min-width: 100px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #0b7dda;
            }
            QPushButton#cancelButton {
                background: #f44336;
            }
            QPushButton#cancelButton:hover {
                background: #d32f2f;
            }
        """)

        # Элементы формы (все с рукописным вводом)
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Автор жалобы")

        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("Содержание жалобы")

        # Диапазон дат
        self.date_from_edit = QDateEdit()
        self.date_from_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_from_edit.setCalendarPopup(True)
        self.date_from_edit.setDate(QDate(1990, 1, 1))

        self.date_to_edit = QDateEdit()
        self.date_to_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_to_edit.setCalendarPopup(True)
        self.date_to_edit.setDate(QDate.currentDate())

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Статус жалобы")

        self.responsible_input = QLineEdit()
        self.responsible_input.setPlaceholderText("Ответственный")

        # Кнопки
        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        # Компоновка
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 10)

        form_layout.addRow("Автор:", self.author_input)
        form_layout.addRow("Содержание:", self.content_input)
        form_layout.addRow("Дата (с):", self.date_from_edit)
        form_layout.addRow("Дата (по):", self.date_to_edit)
        form_layout.addRow("Статус:", self.status_input)
        form_layout.addRow("Ответственный:", self.responsible_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.search_btn)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def get_search_params(self):
        """Возвращает параметры поиска"""
        return {
            'author': self.author_input.text().strip(),
            'content': self.content_input.text().strip(),
            'date_from': self.date_from_edit.date().toString("yyyy-MM-dd"),
            'date_to': self.date_to_edit.date().toString("yyyy-MM-dd"),
            'status': self.status_input.text().strip(),
            'responsible': self.responsible_input.text().strip()
        }