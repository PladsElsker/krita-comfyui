from typing import Dict, cast

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
        self.mapping = {
            name: name
            for name in self.last_docs
        }
    
    def test_mappings(self, mappings: Dict[str, str]) -> bool:
        return len(mappings.keys()) == len(self.last_docs) and all(m in self.last_docs for m in mappings.values())

    def assign_name_mappings(self, mappings: Dict[str, str]):
        if not self.test_mappings(mappings):
            raise ValueError("Unable to retrieve valid unique document id mappings")

        self.mapping = mappings

    def _current_doc_names(self) -> tuple[str, ...]:
        return tuple(doc.name() for doc in self._krita.documents())

    def _check_for_changes(self):
        current_docs = self._current_doc_names()
        if current_docs != self.last_docs:
            self.last_docs = current_docs
            self.on_documents_changed.emit()
