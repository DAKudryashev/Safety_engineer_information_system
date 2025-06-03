from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QPushButton)
from PyQt5.QtCore import Qt


class SearchEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск сотрудников")
        self.setFixedSize(550, 600)  # Вернули исходный размер

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
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #aaa;
                border-radius: 4px;
                min-width: 200px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                min-width: 350px;
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
        self.name_input.setPlaceholderText("Фамилия Имя Отчество")

        self.passport_series_input = QLineEdit()
        self.passport_series_input.setPlaceholderText("Серия паспорта")

        self.passport_number_input = QLineEdit()
        self.passport_number_input.setPlaceholderText("Номер паспорта")

        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("Должность")

        self.instruction_result_input = QLineEdit()
        self.instruction_result_input.setPlaceholderText("Результат инструктажа")

        self.briefing_input = QLineEdit()
        self.briefing_input.setPlaceholderText("Инструктаж")

        self.exam_input = QLineEdit()
        self.exam_input.setPlaceholderText("Экзамен на допуск")

        self.exam_result_input = QLineEdit()
        self.exam_result_input.setPlaceholderText("Результат экзамена")

        self.medical_exam_input = QLineEdit()
        self.medical_exam_input.setPlaceholderText("Медосмотр")

        self.medical_result_input = QLineEdit()
        self.medical_result_input.setPlaceholderText("Результат медосмотра")

        # Кнопки
        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        # Компоновка (как в оригинале)
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(20, 20, 20, 10)

        form_layout.addRow("ФИО:", self.name_input)
        form_layout.addRow("Серия паспорта:", self.passport_series_input)
        form_layout.addRow("Номер паспорта:", self.passport_number_input)
        form_layout.addRow("Должность:", self.position_input)
        form_layout.addRow("Результат инструктажа:", self.instruction_result_input)
        form_layout.addRow("Инструктаж:", self.briefing_input)
        form_layout.addRow("Экзамен на допуск:", self.exam_input)
        form_layout.addRow("Результат экзамена:", self.exam_result_input)
        form_layout.addRow("Медосмотр:", self.medical_exam_input)
        form_layout.addRow("Результат медосмотра:", self.medical_result_input)

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
        """Возвращает критерии поиска в виде словаря"""
        return {
            "name": self.name_input.text().strip(),
            "passport_series": self.passport_series_input.text().strip(),
            "passport_number": self.passport_number_input.text().strip(),
            "position": self.position_input.text().strip(),
            "instruction_result": self.instruction_result_input.text().strip(),
            "briefing": self.briefing_input.text().strip(),
            "exam": self.exam_input.text().strip(),
            "exam_result": self.exam_result_input.text().strip(),
            "medical_exam": self.medical_exam_input.text().strip(),
            "medical_result": self.medical_result_input.text().strip()
        }
