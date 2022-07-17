import sys
from controllers.gui_controller import make_ascii_art, write

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QMessageBox,
    QFileDialog,
    QApplication,
    QPushButton,
    QGridLayout,
    QWidget,
    QLabel,
    QDialog,
    QFormLayout,
    QScrollArea
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


class Window(QMainWindow):
    def __init__(self, app):
        super(Window, self).__init__()
        self.app = app

        self.setWindowTitle('ASCII Art')
        self.init_center_geometry()

        self.image_button = self.configure_image_button()
        self.settings_button = self.configure_settings_button()
        self.layout = self.configure_grid_layout()
        self.copy_button = self.configure_copy_button()
        self.write_file_button = self.configure_write_file_button()

        self.settings_dialog = None
        self.ascii_art = None
        self.image_label = None
        self.image_path = None

    def show_image_selection_dialog(self):
        self.image_path = QFileDialog.getOpenFileName(
            self,
            'Open file', '/home', 'Image Files (*.png *.jpg *.bmp)'
        )[0]

        if self.image_path == '':
            return

        image = QImage(self.image_path)
        pixmap = QPixmap.fromImage(image)

        width = self.size().width()

        pixmap = pixmap.scaled(
            width // 3,
            int((pixmap.height() / pixmap.width()) * (width // 3))
        )

        if self.image_label is not None:
            self.layout.removeWidget(self.image_label)

        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)

        self.layout.addWidget(self.image_label, 1, 0, 4, 3)
        self.layout.addWidget(self.settings_button, 0, 6, 1, 1)

        self.settings_button.setHidden(False)

    def show_select_settings_dialog(self):
        screen_rect = self.screen().geometry()

        window_height = self.size().height() // 3
        window_width = self.size().width() // 3

        screen_center_x = screen_rect.width() // 2 - window_width // 2
        screen_center_y = screen_rect.height() // 2 - window_height // 2

        self.settings_dialog = ASCIIArtSettingsDialog(
            screen_center_x,
            screen_center_y,
            window_width,
            window_height,
            self.draw_ascii_art
        )

        self.settings_dialog.show()

    def draw_ascii_art(self):
        if self.ascii_art is not None:
            self.layout.removeWidget(self.ascii_art)

        ascii_art = make_ascii_art(
            self.image_path,
            self.settings_dialog.width_text,
            self.settings_dialog.height_text,
            self.settings_dialog.symbols_text
        )

        self.ascii_art = QLabel()
        self.ascii_art.setText(ascii_art)

        self.add_font_style_to_ascii_art()

        self.copy_button.setHidden(False)
        self.write_file_button.setHidden(False)

        scroll = QScrollArea(self)
        scroll.setWidget(self.ascii_art)
        scroll.setWidgetResizable(True)

        self.layout.addWidget(scroll, 1, 3, 4, 3)
        self.layout.addWidget(self.copy_button, 1, 6, 2, 1)
        self.layout.addWidget(self.write_file_button, 3, 6, 2, 1)

    def add_font_style_to_ascii_art(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily('Times')
        font.setStyleHint(QFont.Monospace)

        self.ascii_art.setFont(font)

    def copy_ascii_art_to_clipboard(self):
        clipboard = self.app.clipboard()
        clipboard.setText(self.ascii_art.text())

        QMessageBox.question(
            self,
            'Информация',
            'ASCII Art скопирован в буфер обмена',
            QMessageBox.Ok
        )

    def write_ascii_art_to_file(self):
        file_path = QFileDialog.getExistingDirectory(self)
        write(self.ascii_art.text(), self.image_path, file_path)

        QMessageBox.question(
            self,
            'Информация',
            'ASCII Art создан',
            QMessageBox.Ok
        )

    def init_center_geometry(self):
        screen_rect = self.screen().geometry()

        window_height = int(screen_rect.height() / 1.8)
        window_width = int(screen_rect.width() / 1.5)

        screen_center_x = screen_rect.width() // 2 - window_width // 2
        screen_center_y = screen_rect.height() // 2 - window_height // 2

        self.setGeometry(
            screen_center_x,
            screen_center_y,
            window_width,
            window_height
        )

    def configure_image_button(self):
        image_button = QPushButton(self)
        image_button.setText('Выбрать картинку')
        image_button.clicked.connect(self.show_image_selection_dialog)
        image_button.setFixedHeight(self.size().height() // 10)

        return image_button

    def configure_settings_button(self):
        settings_button = QPushButton(self)
        settings_button.setText('Сделать ASCII Art')
        settings_button.clicked.connect(self.show_select_settings_dialog)
        settings_button.hide()
        settings_button.setFixedHeight(self.size().height() // 10)

        return settings_button

    def configure_copy_button(self):
        copy_button = QPushButton(self)
        copy_button.setText('Скопировать')
        copy_button.clicked.connect(self.copy_ascii_art_to_clipboard)
        copy_button.hide()
        copy_button.setFixedHeight(self.size().height() // 5)

        return copy_button

    def configure_write_file_button(self):
        write_file_button = QPushButton(self)
        write_file_button.setText('Сохранить')
        write_file_button.clicked.connect(self.write_ascii_art_to_file)
        write_file_button.hide()
        write_file_button.setFixedHeight(self.size().height() // 5)

        return write_file_button

    def configure_grid_layout(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(
            self.size().height() // 10,
            self.size().height() // 10,
            self.size().height() // 10,
            self.size().height() // 10
        )

        widget = QWidget()
        self.setCentralWidget(widget)

        layout.addWidget(self.image_button, 0, 0, 1, 6)
        self.centralWidget().setLayout(layout)

        return layout


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = Window(application)
    window.show()
    sys.exit(application.exec_())
