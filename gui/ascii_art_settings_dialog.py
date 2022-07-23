from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLineEdit,
    QMessageBox,
    QPushButton,
    QLabel,
    QDialog,
    QFormLayout
)


class ASCIIArtSettingsDialog(QDialog):
    def __init__(self, x, y, width, height, after_closing_func):
        super(ASCIIArtSettingsDialog, self).__init__()
        self.after_closing_func = after_closing_func

        self.symbols_text = None
        self.width_text = None
        self.height_text = None

        self.setGeometry(x, y, width, height)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Параметры ASCII Art')
        self.setModal(True)

        self.settings_description = QLabel()
        description = 'Если ввести ширину или высоту (что-то одно),' \
                      ' то второе вычислится в соответсвиии с ' \
                      'соотношением сторон исходного изображения'
        self.settings_description.setText(description)

        self.symbols = QLineEdit()
        self.width = QLineEdit()
        self.height = QLineEdit()

        apply_settings_button = QPushButton('Подтвердить')
        apply_settings_button.clicked.connect(self.apply_settings)

        form = self.configure_form_layout(apply_settings_button)
        self.setLayout(form)

    def configure_form_layout(self, apply_settings_button):
        form = QFormLayout()
        form.setSpacing(20)

        form.addRow(self.settings_description)
        form.addRow('Символы:', self.symbols)
        form.addRow('Ширина:', self.width)
        form.addRow('Высота:', self.height)
        form.addRow(apply_settings_button)

        return form

    def apply_settings(self):
        if len(self.symbols.text().rstrip()) == 0:
            problem = 'Некорректные символы'
            problem_text = 'ASCII Art из одних пробелов - ' \
                           'это печально, выберите другие символы'
        elif not str.isdigit(self.width.text()) and self.width.text() != '':
            problem = 'Некорректная ширина'
            problem_text = 'Ширина ASCII Art должна быть ' \
                           'целым положительным числом'
        elif not str.isdigit(self.height.text()) and self.height.text() != '':
            problem = 'Некорректная высота'
            problem_text = 'Высота ASCII Art должна быть ' \
                           'целым положительным числом'
        elif self.width.text() == '' and self.height.text() == '':
            problem = 'Некорректные настройки'
            problem_text = 'Введите высоту или ширину (хотя бы одно)'
        elif self.width.text() != '' and int(self.width.text()) == 0:
            problem = 'Некорректная ширина'
            problem_text = 'Ширина ASCII Art не должна быть равна 0'
        elif self.height.text() != '' and int(self.height.text()) == 0:
            problem = 'Некорректная длина'
            problem_text = 'Длина ASCII Art не должна быть равна 0'
        else:
            if str.isdigit(self.height.text()):
                self.height_text = int(self.height.text())
            if str.isdigit(self.width.text()):
                self.width_text = int(self.width.text())

            self.symbols_text = self.symbols.text()

            self.close()
            self.after_closing_func()
            return

        QMessageBox.question(self, problem, problem_text, QMessageBox.Ok)
