from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLineEdit,
    QMessageBox,
    QPushButton,
    QLabel,
    QDialog,
    QFormLayout
)


class PaintCharDialog(QDialog):
    def __init__(self, x, y, width, height, after_closing_func):
        super(PaintCharDialog, self).__init__()
        self.after_closing_func = after_closing_func

        self.paint_char = None

        self.setGeometry(x, y, width, height)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Параметры рисования')
        self.setModal(True)

        self.settings_description = QLabel()
        description = 'Введите символ для рисования'
        self.settings_description.setText(description)

        self.symbol = QLineEdit()

        apply_char_button = QPushButton('Подтвердить')
        apply_char_button.clicked.connect(self.apply_char)

        form = self.configure_form_layout(apply_char_button)
        self.setLayout(form)

    def configure_form_layout(self, apply_char_button):
        form = QFormLayout()
        form.setSpacing(20)

        form.addRow(self.settings_description)
        form.addRow('Символ:', self.symbol)
        form.addRow(apply_char_button)

        return form

    def apply_char(self):
        if len(self.symbol.text()) != 1:
            problem = 'Некорректный ввод'
            problem_text = 'Введите один символ'
            QMessageBox.question(self, problem, problem_text, QMessageBox.Ok)
            return

        self.paint_char = self.symbol.text()
        self.close()
        self.after_closing_func()
