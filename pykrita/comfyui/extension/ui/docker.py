from krita import DockWidget
from PyQt5.QtWidgets import QVBoxLayout,  QWidget


class ComfyUIDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ComfyUI")

        self.container = QWidget()
        self.main_layout = QVBoxLayout(self.container)

        self.setWidget(self.container)

    def showEvent(self, a0):
        super().showEvent(a0)
        if hasattr(self, "server_url") and self.server_url.value is not None:
            self.load_server(self.server_url.value)

    def canvasChanged(self, canvas):
        pass
