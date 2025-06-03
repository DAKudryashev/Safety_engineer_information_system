from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QDateEdit, QComboBox, QPushButton, QLabel)
from PyQt5.QtCore import QDate, Qt


class InsertComplaintDialog(QDialog):
    def __init__(self, employees, engineers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить жалобу")
        self.setFixedSize(600, 400)

        # Подготовка данных
        self.employees = [item[1] for item in employees]
        self.engineers = [item[1] for item in engineers][1:]

        # Стилизация (сохранена из предыдущей версии)
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
                min-width: 250px;
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

        # Элементы формы (без изменений)
        self.author_combo = QComboBox()
        self.author_combo.addItems(self.employees)
        self.author_combo.view().setMinimumWidth(300)

        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("Опишите жалобу")

        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Статус жалобы")
        self.status_input.setMaxLength(32)

        self.responsible_combo = QComboBox()
        self.responsible_combo.addItems(self.engineers)
        self.responsible_combo.view().setMinimumWidth(300)

        # Надпись об ошибке (упрощенная)
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()
        self.error_label.setText("Заполните все обязательные поля")

        # Кнопки (без изменений)
        self.submit_btn = QPushButton("Добавить")
        self.submit_btn.clicked.connect(self.validate_form)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        # Компоновка (без изменений)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 10)

        form_layout.addRow("Автор*:", self.author_combo)
        form_layout.addRow("Содержание*:", self.content_input)
        form_layout.addRow("Дата*:", self.date_edit)
        form_layout.addRow("Статус*:", self.status_input)
        form_layout.addRow("Ответственный*:", self.responsible_combo)

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
        if (not self.author_combo.currentText() or
            not self.content_input.text().strip() or
            not self.status_input.text().strip() or
            not self.responsible_combo.currentText()):
            self.error_label.show()
            return

        self.error_label.hide()
        self.accept()

    def get_data(self):
        """Возвращает введенные данные (без изменений)"""
        return {
            'author': self.author_combo.currentText(),
            'content': self.content_input.text().strip(),
            'date': self.date_edit.date().toString("yyyy-MM-dd"),
            'status': self.status_input.text().strip(),
            'responsible': self.responsible_combo.currentText()
        }