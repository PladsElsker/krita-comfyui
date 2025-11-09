from typing import cast

from krita import Krita
from PyQt5.QtCore import QObject, pyqtBoundSignal, pyqtSignal, QTimer


class DocumentMonitor(QObject):
    on_documents_changed = cast(pyqtBoundSignal, pyqtSignal())

    def __init__(self, interval_ms=300):
        super().__init__()
        self._krita = Krita.instance()
        self.last_docs = self._current_doc_names()
        self._timer = QTimer()
        self._timer.timeout.connect(self._check_for_changes)
        self._timer.start(interval_ms)

    def _current_doc_names(self) -> tuple[str, ...]:
        return tuple(doc.name() for doc in self._krita.documents())

    def _check_for_changes(self):
        current_docs = self._current_doc_names()
        if current_docs != self.last_docs:
            self.last_docs = current_docs
            self.on_documents_changed.emit()
