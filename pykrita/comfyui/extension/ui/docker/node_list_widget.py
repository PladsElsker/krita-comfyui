from typing import List
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import qDebug

from ...models import Node


class NodeListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(4)
        self.main_layout.addStretch(1)
        self.labels = []

    def rebuild(self, inputs: List[Node], outputs: List[Node]):
        nodes = inputs + outputs

        while self.main_layout.count() > 1:
            item = self.main_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        self.labels.clear()

        for node in nodes:
            qDebug(node.model_dump_json())
            label = QLabel(f"{node.type} ({node.id})")
            self.main_layout.insertWidget(self.main_layout.count() - 1, label)
            self.labels.append(label)
