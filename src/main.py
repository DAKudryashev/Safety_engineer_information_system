import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTabWidget, QFrame, QMessageBox)

from src.dialogs.login_dialog import LoginDialog
from database import DataBase
from src.layouts.documents_layout import DocumentsLayout
from src.layouts.employees_layout import EmployeesLayout
from src.layouts.rooms_layout import RoomsLayout
from src.layouts.briefings_layout import BriefingsLayout
from src.layouts.examinations_layuot import ExaminationsLayout
from src.layouts.med_examinations import MedExaminationsLayout
from src.layouts.equipment_layout import EquipmentLayout
from src.layouts.incidents_layout import IncidentsLayout
from src.layouts.complaints_layout import ComplaintsLayout
from src.layouts.extra_layout import ExtraLayout


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

        # Создаем виджет вкладок и как центральный
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Добавляем вкладку помещений, заполняем содержимое
        self.tab1 = RoomsLayout(self.db)
        self.tab1.fill_rooms_table(self.db.get_rooms())
        self.tabs.addTab(self.tab1, 'Помещения')

        # Добавляем вкладку инструктажей, заполняем содержимое
        self.tab2 = BriefingsLayout()
        self.data = self.db.get_planned_briefings()
        self.tab2.fill_planned_table(self.data)
        self.data = self.db.get_completed_briefings()
        self.tab2.fill_completed_table(self.data)
        self.tabs.addTab(self.tab2, 'Инструктажи')

        # Добавляем вкладку сотрудников, заполняем содержимое
        self.tab3 = EmployeesLayout()
        self.data = self.db.get_employees()
        self.tab3.fill_employees_table(self.data)
        self.tabs.addTab(self.tab3, 'Сотрудники')

        # Добавляем вкладку документов, заполняем содержимое
        self.tab4 = DocumentsLayout()
        self.data = self.db.get_regulatory_documents()
        self.tab4.fill_regulatory_table(self.data)
        self.data = self.db.get_internal_documents()
        self.tab4.fill_internal_table(self.data)
        self.tabs.addTab(self.tab4, 'Документы')

        # Добавляем вкладку допусков, заполняем содержимое
        self.tab5 = ExaminationsLayout()
        self.data = self.db.get_examinations()
        self.tab5.fill_exams_table(self.data)
        self.tabs.addTab(self.tab5, 'Экзамены на допуск')

        # Добавляем вкладку медосмотров, заполняем содержимое
        self.tab6 = MedExaminationsLayout()
        self.data = self.db.get_med_examinations()
        self.tab6.fill_med_exams_table(self.data)
        self.tabs.addTab(self.tab6, 'Медосмотры')

        # Добавляем вкладку оборудования, заполняем содержимое
        self.tab7 = EquipmentLayout()
        self.data = self.db.get_equipment()
        self.tab7.fill_equipment_table(self.data)
        self.tabs.addTab(self.tab7, 'Оборудование')

        # Добавляем вкладку инцидентов, заполняем содержимое
        self.tab8 = IncidentsLayout()
        self.data = self.db.get_incidents()
        self.tab8.fill_incidents_table(self.data)
        self.tabs.addTab(self.tab8, 'Инциденты')

        # Добавляем вкладку жалоб сотрудников, заполняем содержимое
        self.tab9 = ComplaintsLayout()
        self.data = self.db.get_complaints()
        self.tab9.fill_complaints_table(self.data)
        self.tabs.addTab(self.tab9, 'Жалобы сотрудников')

        # Добавляем дополнительную вкладку, заполняем содержимое
        self.tab10 = ExtraLayout()
        self.data = self.db.get_engineers_without_passwords()
        self.tab10.fill_engineers_table(self.data)
        self.tabs.addTab(self.tab10, 'Дополнительно')

        # Показываем login-окно, затемняем окружение
        self.login_dialog.show()
        self.overlay = QFrame(self)
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        self.overlay.show()
        self.login_dialog.login_button.clicked.connect(self.authenticate)

        # Реализуем закрытие окна
        self.tab10.escape_button.clicked.connect(self.exit_app)

        print(self.db is self.tab1.db)

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

    def exit_app(self):
        reply = QMessageBox.question(
            self, 'Подтверждение',
            "Вы действительно хотите выйти?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InformationSys()
    window.show()
    sys.exit(app.exec())
