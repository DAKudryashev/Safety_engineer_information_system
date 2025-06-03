from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QDateEdit, QPushButton, QLabel)
from PyQt5.QtCore import QDate, Qt


class UpdateCompletedDialog(QDialog):
    def __init__(self, current, engineers, documents, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Изменить запись")
        self.setFixedSize(500, 400)

        # Подготовка данных для ComboBox
        self.engineers = [item[1] for item in engineers][1:]
        self.documents = [''] + [item[1] for item in documents]  # Добавляем пустое значение

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
        self.name_input.setPlaceholderText("Введите наименование")
        self.name_input.setText(current[0])

        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("Введите содержание")
        self.content_input.setText(current[1])

        # Виджет выбора даты
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setCalendarPopup(True)
        date = QDate.fromString(current[2], 'dd.MM.yyyy')
        self.date_edit.setDate(date)

        # Выпадающий список с ответственными
        self.responsible_combo = QComboBox()
        self.responsible_combo.addItems(self.engineers)
        index = self.responsible_combo.findText(current[3])
        self.responsible_combo.setCurrentIndex(index)

        # Выпадающий список с документами (с пустым значением)
        self.document_combo = QComboBox()
        self.document_combo.addItems(self.documents)
        index = self.document_combo.findText(current[4])
        self.document_combo.setCurrentIndex(index)

        # Получаем ширину самого широкого элемента
        fm = self.document_combo.fontMetrics()
        max_width = max(fm.width(text) for text in [self.document_combo.itemText(i)
                                                    for i in range(self.document_combo.count())])

        # Устанавливаем ширину с небольшим запасом
        self.document_combo.view().setMinimumWidth(max_width + 50)

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

        form_layout.addRow("Наименование*:", self.name_input)
        form_layout.addRow("Содержание*:", self.content_input)
        form_layout.addRow("Дата проведения*:", self.date_edit)
        form_layout.addRow("Ответственный*:", self.responsible_combo)
        form_layout.addRow("Документация:", self.document_combo)

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
        if not self.name_input.text().strip() or not self.content_input.text().strip():
            self.error_label.setText("Заполните все поля со *!")
            self.error_label.show()
            return

        self.error_label.hide()
        self.accept()

    def get_data(self):
        """Возвращает введенные данные в структурированном виде"""
        return [
            self.name_input.text().strip(),
            self.content_input.text().strip(),
            self.date_edit.date().toString("yyyy-MM-dd"),
            self.responsible_combo.currentText(),
            self.document_combo.currentText()
        ] if self.document_combo.currentText() else [
            self.name_input.text().strip(),
            self.content_input.text().strip(),
            self.date_edit.date().toString("yyyy-MM-dd"),
            self.responsible_combo.currentText()
        ]