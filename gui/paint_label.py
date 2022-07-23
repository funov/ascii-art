from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QPen
from PyQt5.QtWidgets import QLabel


class PaintLabel(QLabel):
    def __init__(self, canvas, ascii_art, width_coefficient, height_coefficient, pixmap_coefficient):
        super(PaintLabel, self).__init__()
        self.width_coefficient = width_coefficient
        self.height_coefficient = height_coefficient
        self.setPixmap(canvas)

        self.pixels = ascii_art
        self.pixels_width = int(canvas.width() / width_coefficient / pixmap_coefficient)
        self.pixels_height = int(canvas.height() / height_coefficient / pixmap_coefficient)

        self.is_rubber = False
        self.is_pencil = False

        self.pencil_char = '@'

        self.draw_ascii_art()

    def draw_ascii_art(self):
        painter = self.get_painter()

        for w in range(1, self.pixels_width + 1):
            for h in range(1, self.pixels_height + 1):
                painter.drawText(w * self.width_coefficient, h * self.height_coefficient, self.pixels[h - 1][w - 1])

        painter.end()
        self.update()

    def mouseMoveEvent(self, e):
        if self.is_pencil or self.is_rubber:
            self.draw(e)

    def draw(self, e):
        painter = self.get_painter()

        pen = QPen(Qt.white)
        painter.setPen(pen)

        a = e.x() - e.x() % self.width_coefficient
        b = e.y() - e.y() % self.height_coefficient
        c = e.x() // self.width_coefficient
        d = e.y() // self.height_coefficient

        if not 0 < c < self.pixels_width + 1 or not 0 < d < self.pixels_height + 1:
            return

        if self.pixels[d - 1][c - 1] != ' ':
            for i in range(10):
                painter.drawText(a, b, self.pixels[d - 1][c - 1])

        self.pixels[d - 1][c - 1] = ' '

        if self.is_pencil:
            pen = QPen(Qt.black)
            painter.setPen(pen)

            painter.drawText(a, b, self.pencil_char)

            self.pixels[d - 1][c - 1] = self.pencil_char

        painter.end()
        self.update()

    def get_painter(self):
        painter = QPainter(self.pixmap())

        pen = QPen(Qt.black)
        painter.setPen(pen)

        font = QFont()
        font.setPointSize(10)
        font.setFamily('Times')
        font.setStyleHint(QFont.Monospace)
        painter.setFont(font)

        return painter
