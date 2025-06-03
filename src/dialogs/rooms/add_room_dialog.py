from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
                             QComboBox, QDateEdit, QPushButton, QLabel)
from PyQt5.QtCore import QDate, Qt


class AddRowDialog(QDialog):
    def __init__(self, engineers, parent=None):
        super().__init__(parent)
        self.names = [row[1] for row in engineers][1:]
        self.setWindowTitle("Добавить запись")
        self.setFixedSize(450, 350)

        # Стилизация диалога
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
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #aaa;
                border-radius: 4px;
                min-width: 200px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                min-width: 300px;
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
            #errorLabel {
                color: red;
                font-weight: normal;
                margin-top: 10px;
            }
        """)

        # Элементы формы
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите наименование")
        self.name_input.setMaxLength(32)  # Ограничение 32 символа

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Введите состояние")
        self.status_input.setMaxLength(16)  # Ограничение 16 символов

        # Виджет выбора даты
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        # Выпадающий список с ответственными (с увеличенной шириной)
        self.responsible_combo = QComboBox()
        self.responsible_combo.addItems(self.names)
        self.responsible_combo.view().setMinimumWidth(300)  # Ширина выпадающего списка

        # Надпись об ошибке
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()

        # Кнопки
        self.submit_btn = QPushButton("Добавить")
        self.submit_btn.clicked.connect(self.validate_form)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        # Компоновка
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 10)

        form_layout.addRow("Наименование:", self.name_input)
        form_layout.addRow("Состояние:", self.status_input)
        form_layout.addRow("Дата проверки:", self.date_edit)
        form_layout.addRow("Ответственный:", self.responsible_combo)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.submit_btn)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.error_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def validate_form(self):
        """Проверяет заполнение всех полей"""
        if (not self.name_input.text().strip() or
                not self.status_input.text().strip()):
            self.error_label.setText("Заполните все поля!")
            self.error_label.show()
            return

        self.error_label.hide()
        self.accept()

    def get_data(self):
        """Возвращает введенные данные"""
        return [
            self.name_input.text().strip(),
            self.status_input.text().strip(),
            self.date_edit.date().toString("yyyy-MM-dd"),
            self.responsible_combo.currentText()]
