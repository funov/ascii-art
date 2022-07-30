import sys
from controllers.gui_controller import make_ascii_art, write
from ascii_art_settings_dialog import ASCIIArtSettingsDialog
from get_paint_char_dialog import PaintCharDialog
from paint_label import PaintLabel

from PyQt5.QtCore import Qt, QThreadPool, QRunnable, pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QApplication,
    QPushButton,
    QGridLayout,
    QWidget,
    QLabel,
    QScrollArea
)


class Window(QMainWindow):
    def __init__(self, app):
        super(Window, self).__init__()
        self.app = app

        self.setWindowTitle('ASCII Art')
        self.init_center_geometry()

        self.image_button = self.configure_button(
            'Выбрать картинку',
            self.show_image_selection_dialog,
            False
        )
        self.settings_button = self.configure_button(
            'Сделать ASCII Art',
            self.show_select_settings_dialog,
            True
        )
        self.copy_button = self.configure_button(
            'Скопировать',
            self.copy_ascii_art_to_clipboard,
            True
        )
        self.write_file_button = self.configure_button(
            'Сохранить',
            self.write_ascii_art_to_file,
            True
        )
        self.pencil_button = self.configure_button(
            'Карандаш',
            self.use_pencil,
            True
        )
        self.rubber_button = self.configure_button(
            'Резинка',
            self.use_rubber,
            True
        )

        self.grid_layout = self.configure_grid_layout()

        self.settings_dialog = None
        self.paint_char_dialog = None
        self.ascii_art = None
        self.image_label = None
        self.image_path = None
        self.threadpool = None

    def show_image_selection_dialog(self):
        image_path = QFileDialog.getOpenFileName(
            self,
            'Open file', '/home', 'Image Files (*.png *.jpg *.bmp)'
        )[0]

        if image_path == '':
            return

        self.image_path = image_path

        image = QImage(self.image_path)
        pixmap = QPixmap.fromImage(image)

        width = self.size().width()

        pixmap = pixmap.scaled(
            width // 3,
            int((pixmap.height() / pixmap.width()) * (width // 3))
        )

        if self.image_label is not None:
            self.grid_layout.removeWidget(self.image_label)

        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)

        self.grid_layout.addWidget(self.image_label, 1, 0, 4, 3)
        self.grid_layout.addWidget(self.settings_button, 0, 6, 1, 1)

        self.settings_button.setHidden(False)

    def show_select_settings_dialog(self):
        pos_x, pos_y, window_w, window_h = self.get_dialog_params()

        self.settings_dialog = ASCIIArtSettingsDialog(
            pos_x,
            pos_y,
            window_w,
            window_h,
            self.get_ascii_art
        )

        self.settings_dialog.show()

    def draw_ascii_art_trigger(self, ascii_art_list):
        self.draw_ascii_art(ascii_art_list)

    def get_ascii_art(self):
        self.threadpool = QThreadPool()

        worker = MakeASCIIArtWorker(
            self.image_path,
            self.settings_dialog.width_text,
            self.settings_dialog.height_text,
            self.settings_dialog.symbols_text,
        )

        worker.signals.result.connect(self.draw_ascii_art_trigger)

        self.threadpool.start(worker)

    def draw_ascii_art(self, ascii_art_list):
        w_coefficient = 12
        h_coefficient = w_coefficient * 2
        pixmap_coefficient = 1.1

        canvas = QPixmap(
            int(len(ascii_art_list[0]) * w_coefficient * pixmap_coefficient),
            int(len(ascii_art_list) * h_coefficient * pixmap_coefficient)
        )

        canvas.fill(Qt.white)

        self.ascii_art = PaintLabel(
            canvas,
            ascii_art_list,
            w_coefficient,
            h_coefficient,
            pixmap_coefficient
        )

        self.ascii_art.draw_ascii_art()

        self.copy_button.setHidden(False)
        self.write_file_button.setHidden(False)
        self.pencil_button.setHidden(False)
        self.rubber_button.setHidden(False)

        scroll = QScrollArea(self)
        scroll.setWidget(self.ascii_art)
        scroll.setWidgetResizable(True)

        self.grid_layout.addWidget(scroll, 1, 3, 4, 3)
        self.grid_layout.addWidget(self.copy_button, 1, 6, 1, 1)
        self.grid_layout.addWidget(self.write_file_button, 2, 6, 1, 1)
        self.grid_layout.addWidget(self.pencil_button, 3, 6, 1, 1)
        self.grid_layout.addWidget(self.rubber_button, 4, 6, 1, 1)

    def copy_ascii_art_to_clipboard(self):
        clipboard = self.app.clipboard()
        ascii_text = '\n'.join([''.join(x) for x in self.ascii_art.pixels])
        clipboard.setText(ascii_text)

        QMessageBox.question(
            self,
            'Информация',
            'ASCII Art скопирован в буфер обмена',
            QMessageBox.Ok
        )

    def use_pencil(self):
        self.ascii_art.is_rubber = False
        self.ascii_art.is_pencil = True

        pos_x, pos_y, window_w, window_h = self.get_dialog_params()

        self.paint_char_dialog = PaintCharDialog(
            pos_x,
            pos_y,
            window_w,
            window_h,
            self.apply_char
        )

        self.paint_char_dialog.show()

    def get_dialog_params(self):
        screen_rect = self.screen().geometry()

        window_height = self.size().height() // 2
        window_width = self.size().width() // 2

        screen_center_x = screen_rect.width() // 2 - window_width // 2
        screen_center_y = screen_rect.height() // 2 - window_height // 2

        return screen_center_x, screen_center_y, window_width, window_height

    def apply_char(self):
        self.ascii_art.pencil_char = self.paint_char_dialog.paint_char

    def use_rubber(self):
        self.ascii_art.is_rubber = True
        self.ascii_art.is_pencil = False

    def write_ascii_art_to_file(self):
        file_path = QFileDialog.getExistingDirectory(self)

        if file_path == '':
            return

        ascii_lines = [''.join(x) for x in self.ascii_art.pixels]
        ascii_art_text = '\n'.join(ascii_lines)
        write(ascii_art_text, self.image_path, file_path)

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

    def configure_button(self, title, action, is_hide):
        button = QPushButton(self)
        button.setText(title)
        button.clicked.connect(action)

        if is_hide:
            button.hide()

        button.setFixedHeight(self.size().height() // 10)

        return button

    def configure_grid_layout(self):
        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(
            self.size().height() // 10,
            self.size().height() // 10,
            self.size().height() // 10,
            self.size().height() // 10
        )

        widget = QWidget()
        self.setCentralWidget(widget)

        grid_layout.addWidget(self.image_button, 0, 0, 1, 6)
        self.centralWidget().setLayout(grid_layout)

        return grid_layout


class MakeASCIIArtWorker(QRunnable):
    def __init__(self, image_path, width_text, height_text, symbols_text):
        super(MakeASCIIArtWorker, self).__init__()
        self.image_path = image_path
        self.width_text = width_text
        self.height_text = height_text
        self.symbols_text = symbols_text

        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        ascii_art = make_ascii_art(
            self.image_path,
            self.width_text,
            self.height_text,
            self.symbols_text
        )

        self.signals.result.emit(ascii_art)


class WorkerSignals(QObject):
    result = pyqtSignal(object)


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = Window(application)
    window.show()
    sys.exit(application.exec_())
