from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QDateEdit, QPushButton, QLabel,
                             QComboBox, QFileDialog)
from PyQt5.QtCore import QDate, Qt


class UpdateIncidentDialog(QDialog):
    def __init__(self, current, engineers, employees, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Изменить инцидент")
        self.setFixedSize(700, 450)

        # Подготовка данных
        self.engineers = [item[1] for item in engineers][1:]
        self.employees = [item[1] for item in employees]

        # Стилизация (единый стиль)
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
            QPushButton#browseButton {
                background: #2196F3;
            }
            QPushButton#browseButton:hover {
                background: #0b7dda;
            }
            #errorLabel {
                color: red;
                font-weight: normal;
                margin-top: 10px;
                margin-bottom: 10px;
            }
        """)

        # Элементы формы
        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("Опишите инцидент")
        self.content_input.setText(current[0])

        # Дата происшествия
        self.incident_date_edit = QDateEdit()
        self.incident_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.incident_date_edit.setCalendarPopup(True)
        data = QDate.fromString(current[1], 'dd.MM.yyyy')
        self.incident_date_edit.setDate(data)

        # Ответственный (обязательное поле)
        self.responsible_combo = QComboBox()
        self.responsible_combo.addItems(self.engineers)
        if self.engineers:
            index = self.responsible_combo.findText(current[2])
            self.responsible_combo.setCurrentIndex(index)
        self.responsible_combo.view().setMinimumWidth(300)

        # Участник (не обязательное поле)
        self.participant_combo = QComboBox()
        self.participant_combo.addItem("")  # Пустой элемент
        self.participant_combo.addItems(self.employees)
        index = self.participant_combo.findText(current[3])
        self.participant_combo.setCurrentIndex(index)
        self.participant_combo.view().setMinimumWidth(300)

        # Поле для фото
        self.photo_path_input = QLineEdit()
        self.photo_path_input.setPlaceholderText("Путь к файлу с фото")
        self.photo_path_input.setText(current[4])
        self.browse_btn = QPushButton("Обзор")
        self.browse_btn.setObjectName("browseButton")
        self.browse_btn.clicked.connect(self.browse_photo)

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

        form_layout.addRow("Содержание*:", self.content_input)
        form_layout.addRow("Дата происшествия*:", self.incident_date_edit)
        form_layout.addRow("Ответственный*:", self.responsible_combo)
        form_layout.addRow("Участник:", self.participant_combo)

        # Специальная строка для фото с кнопкой обзора
        photo_layout = QHBoxLayout()
        photo_layout.addWidget(self.photo_path_input)
        photo_layout.addWidget(self.browse_btn)
        form_layout.addRow("Фото:", photo_layout)

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

    def browse_photo(self):
        """Открывает диалог выбора файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите фото", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.photo_path_input.setText(file_path)

    def validate_form(self):
        """Проверяет заполнение обязательных полей"""
        if not self.content_input.text().strip() or not self.responsible_combo.currentText():
            self.error_label.setText("Заполните обязательные поля (помеченные *)!")
            self.error_label.show()
            return

        self.error_label.hide()
        self.accept()

    def get_data(self):
        """Возвращает введенные данные"""
        return {
            'content': self.content_input.text().strip(),
            'incident_date': self.incident_date_edit.date().toString("yyyy-MM-dd"),
            'responsible': self.responsible_combo.currentText(),
            'participant': self.participant_combo.currentText() if self.participant_combo.currentText() else None,
            'photo_path': self.photo_path_input.text().strip() if self.photo_path_input.text().strip() else None
        }