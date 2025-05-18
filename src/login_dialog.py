from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
import sys


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Авторизация")
        self.setFixedSize(550, 330)

        # Стилизация диалога
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QDialog {
                background: #f5f5f5;
                border: 2px solid #444;
                border-radius: 8px;
            }
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)

        # Элементы формы
        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Надпись о неверных данных
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()

        # Кнопка входа
        self.login_button = QPushButton("Войти")

        # Компоновка
        layout = QVBoxLayout()

        username_layout = QVBoxLayout()
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_input)

        password_layout = QVBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.login_button)

        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.error_label)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            # Игнорируем нажатие Escape
            event.ignore()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication([])

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        # Если авторизация успешна
        QMessageBox.information(None, "Успех", "Авторизация прошла успешно!")
    else:
        # Если диалог был закрыт или авторизация не удалась
        QMessageBox.warning(None, "Выход", "Авторизация не выполнена")

    sys.exit(app.exec())
