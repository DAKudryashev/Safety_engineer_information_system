import sys
import webbrowser
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTabWidget, QFrame, QMessageBox,
                             QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

from login_dialog import LoginDialog
from database import DataBase
from documents_layout import DocumentsLayout
from employee_layout import EmployeeLayout


class InformationSys(QMainWindow):
    def __init__(self):
        super(InformationSys, self).__init__()

        # Подключаем БД
        self.db = DataBase()
        self.engineers = self.db.get_engineers()

        # Устанавливаем параметры главного окна
        self.setWindowTitle("Система инженера безопасности")
        self.setGeometry(100, 100, 400, 300)
        self.showFullScreen()
        self.login_dialog = LoginDialog(self)

        # Создаем виджет вкладок и устанавливаем виджет вкладок как центральный
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab2 = EmployeeLayout()
        self.tabs.addTab(self.tab2, 'Сотрудники')

        self.tab3 = DocumentsLayout()
        self.data = self.db.get_regulatory_documents()
        self.tab3.fill_regulatory_table(self.data)
        self.data = self.db.get_internal_documents()
        self.tab3.fill_internal_documents(self.data)
        self.tabs.addTab(self.tab3, 'Документы')
        # # Создаем несколько вкладок
        # self.tab1 = QWidget()
        # self.tab2 = QWidget()
        # self.tab3 = QWidget()
        #
        # # Добавляем содержимое на вкладки
        # self.tab1.layout = QVBoxLayout()
        # self.tab1.layout.addWidget(QLabel("Содержимое первой вкладки"))
        # self.tab1.setLayout(self.tab1.layout)
        #
        # self.tab2.layout = QVBoxLayout()
        # self.tab2.layout.addWidget(QLabel("Содержимое второй вкладки"))
        # self.tab2.setLayout(self.tab2.layout)
        #
        # # Добавляем вкладки в виджет
        # self.tabs.addTab(self.tab1, "Сотрудники")
        # self.tabs.addTab(self.tab2, "Инструктажи")
        # self.tabs.addTab(self.tab3, "Документы")

        # Показываем login-окно, затемняем окружение
        self.login_dialog.show()
        self.overlay = QFrame(self)
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        self.overlay.show()
        self.login_dialog.login_button.clicked.connect(self.authenticate)

    def authenticate(self):
        """Проверка учетных данных"""
        username = self.login_dialog.username_input.text().strip()
        password = self.login_dialog.password_input.text().strip()

        for i in range(len(self.engineers)):
            if username == self.engineers[i][1] and password == self.engineers[i][2]:
                QMessageBox.information(None, "Успех", "Авторизация прошла успешно!")
                self.login_dialog.accept()
                self.overlay.hide()
        else:
            self.login_dialog.error_label.setText("Неверное имя пользователя или пароль")
            self.login_dialog.error_label.show()
            self.login_dialog.password_input.clear()
            self.login_dialog.username_input.clear()
            self.login_dialog.username_input.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InformationSys()
    window.show()
    sys.exit(app.exec())
