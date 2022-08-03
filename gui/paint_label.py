from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QPen
from PyQt5.QtWidgets import QLabel


class PaintLabel(QLabel):
    def __init__(self,
                 canvas,
                 ascii_art,
                 width_coef,
                 height_coef,
                 pixmap_coef,
                 font_size):
        super(PaintLabel, self).__init__()
        self.width_coef = width_coef
        self.height_coef = height_coef
        self.font_size = font_size
        self.setPixmap(canvas)

        self.pixels = ascii_art
        self.pixels_width = int(canvas.width() / width_coef / pixmap_coef)
        self.pixels_height = int(canvas.height() / height_coef / pixmap_coef)

        self.is_rubber = False
        self.is_pencil = False

        self.pencil_char = None

    def draw_ascii_art(self):
        painter = self.get_painter()

        for w in range(1, self.pixels_width + 1):
            for h in range(1, self.pixels_height + 1):
                painter.drawText(
                    w * self.width_coef,
                    h * self.height_coef,
                    self.pixels[h - 1][w - 1]
                )

        painter.end()
        self.update()

    def mouseMoveEvent(self, e):
        if self.is_pencil or self.is_rubber:
            self.edit_ascii_art(e)

    def edit_ascii_art(self, e):
        painter = self.get_painter()

        pen = QPen(Qt.white)
        painter.setPen(pen)

        x_pixel = e.x() - e.x() % self.width_coef
        y_pixel = e.y() - e.y() % self.height_coef
        column_ind = int(e.x() / self.width_coef)
        row_ind = int(e.y() / self.height_coef)

        is_column_correct = not 0 < column_ind < self.pixels_width + 1
        is_row_correct = not 0 < row_ind < self.pixels_height + 1

        if is_column_correct or is_row_correct:
            return

        if self.pixels[row_ind - 1][column_ind - 1] != ' ':
            for i in range(10):
                painter.drawText(
                    x_pixel,
                    y_pixel,
                    self.pixels[row_ind - 1][column_ind - 1]
                )

        self.pixels[row_ind - 1][column_ind - 1] = ' '

        if self.is_pencil:
            pen = QPen(Qt.black)
            painter.setPen(pen)

            painter.drawText(x_pixel, y_pixel, self.pencil_char)

            self.pixels[row_ind - 1][column_ind - 1] = self.pencil_char

        painter.end()
        self.update()

    def get_painter(self):
        painter = QPainter(self.pixmap())

        pen = QPen(Qt.black)
        painter.setPen(pen)

        font = QFont()
        font.setPointSize(self.font_size)
        font.setFamily('Times')
        font.setStyleHint(QFont.Monospace)
        painter.setFont(font)

        return painter
