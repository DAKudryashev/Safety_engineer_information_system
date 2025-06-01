from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QPushButton, QLabel)
from PyQt5.QtCore import Qt


class UpdateEmployeeDialog(QDialog):
    def __init__(self, current, briefings, exams, medical_exams, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить сотрудника")
        self.setFixedSize(550, 600)

        # Подготовка данных для ComboBox
        self.briefings = [''] + [item[1] for item in briefings]
        self.exams = [''] + [item[1] for item in exams]
        self.medical_exams = [''] + [item[1] for item in medical_exams]

        # Стилизация (сохраняем ваш стиль)
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
            QLineEdit, QComboBox {
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
        self.name_input.setMaxLength(128)
        self.name_input.setText(current[0])

        self.passport_series_input = QLineEdit()
        self.passport_series_input.setPlaceholderText("** **")
        self.passport_series_input.setInputMask("99 99")
        self.passport_series_input.setMaxLength(5)
        self.passport_series_input.setText(current[1])

        self.passport_number_input = QLineEdit()
        self.passport_number_input.setPlaceholderText("******")
        self.passport_number_input.setInputMask("999999")
        self.passport_number_input.setMaxLength(6)
        self.passport_number_input.setText(current[2])

        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("Должность")
        self.position_input.setMaxLength(128)
        self.position_input.setText(current[3])

        self.instruction_result_input = QLineEdit()
        self.instruction_result_input.setPlaceholderText("Результат инструктажа")
        self.instruction_result_input.setMaxLength(32)
        self.instruction_result_input.setText(current[4])

        # Выпадающие списки
        self.briefing_combo = QComboBox()
        self.briefing_combo.addItems(self.briefings)
        index = self.briefing_combo.findText(current[5])
        self.briefing_combo.setCurrentIndex(index)

        self.exam_combo = QComboBox()
        self.exam_combo.addItems(self.exams)
        index = self.exam_combo.findText(current[6])
        self.exam_combo.setCurrentIndex(index)

        self.medical_exam_combo = QComboBox()
        self.medical_exam_combo.addItems(self.medical_exams)
        index = self.medical_exam_combo.findText(current[8])
        self.medical_exam_combo.setCurrentIndex(index)

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
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(20, 20, 20, 10)

        form_layout.addRow("ФИО:", self.name_input)
        form_layout.addRow("Серия паспорта:", self.passport_series_input)
        form_layout.addRow("Номер паспорта:", self.passport_number_input)
        form_layout.addRow("Должность:", self.position_input)
        form_layout.addRow("Результат инструктажа:", self.instruction_result_input)
        form_layout.addRow("Инструктаж:", self.briefing_combo)
        form_layout.addRow("Экзамен:", self.exam_combo)
        form_layout.addRow("Медосмотр:", self.medical_exam_combo)

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
        """Проверяет заполнение обязательных полей"""
        errors = []

        if not self.name_input.text().strip():
            errors.append("ФИО")

        if len(self.passport_series_input.text().replace(" ", "")) != 4:
            errors.append("Серия паспорта")

        if len(self.passport_number_input.text()) != 6:
            errors.append("Номер паспорта")

        if not self.position_input.text().strip():
            errors.append("Должность")

        if errors:
            self.error_label.setText(f"Заполните: {', '.join(errors)}")
            self.error_label.show()
            return

        self.error_label.hide()
        self.accept()

    def get_data(self):
        """Возвращает введенные данные в структурированном виде"""
        return {
            "name": self.name_input.text().strip(),
            "passport_series": self.passport_series_input.text(),
            "passport_number": self.passport_number_input.text(),
            "position": self.position_input.text().strip(),
            "instruction_result": self.instruction_result_input.text().strip(),
            "briefing": self.briefing_combo.currentText() if self.briefing_combo.currentIndex() > 0 else None,
            "exam": self.exam_combo.currentText() if self.exam_combo.currentIndex() > 0 else None,
            "medical_exam": self.medical_exam_combo.currentText() if self.medical_exam_combo.currentIndex() > 0 else None
        }