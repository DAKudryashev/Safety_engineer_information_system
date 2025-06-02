from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QDateEdit, QPushButton, QLabel, QComboBox)
from PyQt5.QtCore import QDate, Qt


class UpdateInternalDialog(QDialog):
    def __init__(self, current, engineers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить документ")
        self.setFixedSize(500, 350)  # Немного больше из-за дополнительного поля

        # Подготовка данных для ComboBox с ФИО
        self.engineers = [row[1] for row in engineers][1:]

        # Стилизация (сохраняем как в предыдущем диалоге)
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
        self.name_input.setPlaceholderText("Введите название документа")
        self.name_input.setText(current[0])

        # Виджет выбора даты
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setCalendarPopup(True)
        data = QDate.fromString(current[1], 'dd.MM.yyyy')
        self.date_edit.setDate(QDate.currentDate())

        # Выпадающий список с ФИО
        self.responsible_combo = QComboBox()
        self.responsible_combo.addItems(self.engineers)
        if self.engineers:
            index = self.responsible_combo.findText(current[2])
            self.responsible_combo.setCurrentIndex(index)
        self.responsible_combo.view().setMinimumWidth(300)

        # Поле для пути к файлу
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("Укажите путь к файлу")
        self.file_path_input.setText(current[3])

        # Надпись об ошибке
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
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

        form_layout.addRow("Название документа:", self.name_input)
        form_layout.addRow("Дата создания:", self.date_edit)
        form_layout.addRow("Добавил:", self.responsible_combo)
        form_layout.addRow("Путь к файлу:", self.file_path_input)

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
                not self.file_path_input.text().strip() or
                (self.engineers and not self.responsible_combo.currentText())):
            self.error_label.setText("Заполните все поля!")
            self.error_label.show()
            return

        self.error_label.hide()
        self.accept()

    def get_data(self):
        """Возвращает введенные данные в структурированном виде"""
        return {
            'name': self.name_input.text().strip(),
            'date': self.date_edit.date().toString("yyyy-MM-dd"),
            'responsible': self.responsible_combo.currentText(),
            'file_path': self.file_path_input.text().strip()
        }