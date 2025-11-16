from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QTableWidget

from database import DataBase


class BaseLayout(QHBoxLayout):
    def __init__(self, db: DataBase):
        super().__init__()

        # Таблица слоя
        self.table = QTableWidget()
        # Подслой с кнопками
        self.buttons_layout = QVBoxLayout()
        # Предоставление доступа к экземпляру класса db
        self.db = db

    def setup_buttons_layout(self):
        """Формирует подслой с кнопками"""
        pass

    def setup_table(self, data):
        """Формирует таблицу"""
        pass

    def setup_ui(self):
        """Устанавливает настройки визуальных элементов для этого слоя"""
        pass

    def search_button_clicked(self):
        """Функция, работающая при нажатии клавиши 'Найти'"""
        pass

    def insert_button_clicked(self):
        """Функция, работающая при нажатии клавиши 'Добавить'"""
        pass

    def update_button_clicked(self):
        """Функция, работающая при нажатии клавиши 'Изменить'"""
        pass

    def delete_button_clicked(self):
        """Функция, работающая при нажатии клавиши 'Удалить'"""
        pass

    def reset_button_clicked(self):
        """Функция, работающая при нажатии клавиши 'Обновить'"""
        pass

