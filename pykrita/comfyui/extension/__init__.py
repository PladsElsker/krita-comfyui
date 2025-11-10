from krita import Extension, DockWidgetFactory, DockWidgetFactoryBase, Krita

from .config import Config
from .comfy_websocket import ComfyWebsocket
from .comfy_krita_bridge import ComfyKritaBridge
from .document_monitor import DocumentMonitor
from .ui.connection import ComfyUIWebsocketConnectionDialog
from .ui.docker import ComfyUIDocker


class ComfyUIExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.comfy_ws = ComfyWebsocket()
        self.document_monitor = DocumentMonitor()
        self.bridge = ComfyKritaBridge(self.comfy_ws, self.document_monitor)
        self.config = Config()

        self.document_monitor.on_documents_changed.connect(self.bridge.update_documents)

        ComfyUIWebsocketConnectionDialog(
            comfy_ws=self.comfy_ws, 
            config=self.config
        ).connect()

        self.docker_factory = DockWidgetFactory(
            "comfyui_docker",
            DockWidgetFactoryBase.DockPosition.DockRight,
            ComfyUIDocker
        )
        Krita.instance().addDockWidgetFactory(self.docker_factory)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction(
            "ComfyUISetup-15347", "ComfyUI...", "settings", 
        )
        action.triggered.connect(self.open_config)

    def open_config(self):
        dialog = ComfyUIWebsocketConnectionDialog(comfy_ws=self.comfy_ws, config=self.config)
        dialog.exec_()
