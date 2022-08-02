from controllers.gui_controller import make_ascii_art
from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


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


class DrawASCIIArtWorker(QRunnable):
    def __init__(self, main_window):
        super(DrawASCIIArtWorker, self).__init__()
        self.main_window = main_window

        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.main_window.ascii_art.draw_ascii_art()
        self.signals.finished.emit()


class WorkerSignals(QObject):
    result = pyqtSignal(object)
    finished = pyqtSignal()
