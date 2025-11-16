from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from main_window_tabs.base_layout import BaseLayout

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
        """Заполняет основной слой готовыми подслоями"""
        if self.tab_layout.count() != 0:
            raise Exception('На вкладке уже есть элементы')

        for label, layout in layouts.items():
            self.tab_layout.addWidget(QLabel(label))
            self.tab_layout.addLayout(layout)