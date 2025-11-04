import os
from PyQt5.QtWidgets import QMessageBox

buttons = ['Найти', 'Добавить', 'Изменить', 'Удалить', 'Обновить']

def open_document(file_path):
    """Открывает PDF-файл программой по умолчанию"""
    if os.path.exists(file_path):
        os.startfile(file_path)
    else:
        QMessageBox.warning(None, "Файл не найден", "Указанный путь не содержит файла")
