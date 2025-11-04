from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget

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


class BaseTabWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Основной слой, куда будет добавлена остальная логика
        self.tab_layout = QVBoxLayout()
        self.setLayout(self.tab_layout)

    def setup_ui(self):
        """Устанавливает общие настройки визуальных элементов"""
        self.setStyleSheet("QPushButton { font-size: 11pt; }")

    def set_layouts(self, layouts: dict[str, BaseLayout]):
        """Заполняет готовыми слоями"""
        if self.tab_layout.count() != 0:
            raise Exception('На вкладке уже есть элементы')

        for label, layout in layouts.items():
            self.tab_layout.addWidget(QLabel(label))
            self.tab_layout.addLayout(layout)