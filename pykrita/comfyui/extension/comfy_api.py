from .models import UpdateKritaDocumentsRequest
from .comfy_websocket import ComfyWebsocket
from .document_monitor import DocumentMonitor

from PyQt5.QtCore import qDebug


class ComfyApi:
    def __init__(self, comfy_ws: ComfyWebsocket, document_monitor: DocumentMonitor):
        self.comfy_ws = comfy_ws
        self.document_monitor = document_monitor

    def update_documents(self):
        if self.comfy_ws.sid is None:
            return
        try:
            documents = list(self.document_monitor.last_docs)
            sid = self.comfy_ws.sid
            update_request = UpdateKritaDocumentsRequest(documents=documents)
            self.comfy_ws.put(f"/krita/{sid}/documents", update_request.model_dump())
            qDebug(f"sent {update_request.model_dump()}")
        except Exception as exception:
            qDebug(str(exception))
