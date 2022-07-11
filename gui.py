import sys
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QMessageBox, QFileDialog, QApplication, QPushButton


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('ASCII ART')
        self.__init_center_geometry()
        self.__init_image_button()
        self.__init_apply_ascii_chars_button()
        self.__init_ascii_chars_input()

    def show_dialog(self):
        image_path = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Image Files (*.png *.jpg *.bmp)')[0]

    def apply_chars(self):
        if len(self.text_box.text().rstrip()) != 0:
            text = self.text_box.text()
            QMessageBox.question(self, 'Символы для ASCII ART', text, QMessageBox.Ok, QMessageBox.Ok)

        self.text_box.setText("")

    def __init_center_geometry(self):
        screen_rect = self.screen().geometry()

        self.window_height = int(screen_rect.height() / 1.8)
        self.window_width = int(screen_rect.width() / 1.5)

        screen_center_x = screen_rect.width() // 2 - self.window_width // 2
        screen_center_y = screen_rect.height() // 2 - self.window_height // 2

        self.setGeometry(
            screen_center_x,
            screen_center_y,
            self.window_width,
            self.window_height
        )

    def __init_image_button(self):
        self.image_button = QPushButton(self)
        self.image_button.move(self.window_width // 10, self.window_height // 10)
        self.image_button.setText('Выбрать картинку')
        self.image_button.setFixedWidth(int(self.window_width / 1.5))
        self.image_button.clicked.connect(self.show_dialog)

    def __init_apply_ascii_chars_button(self):
        self.input_button = QPushButton(self)
        self.input_button.move(self.window_width // 10, self.window_height // 5)
        self.input_button.setText('Применить символы')
        self.input_button.setFixedWidth(int(self.window_width / 1.5))
        self.input_button.clicked.connect(self.apply_chars)

    def __init_ascii_chars_input(self):
        self.text_box = QLineEdit(self)
        self.text_box.move(self.window_width // 10, self.window_height // 2)
        self.text_box.resize(int(self.window_width / 1.5), self.window_height // 10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
