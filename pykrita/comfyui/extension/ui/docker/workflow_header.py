from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


class WorkflowHeader(QWidget):
    workflowChanged = pyqtSignal(str)
    refreshRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._workflow_name = None

        self.label = QLabel("Workflow: —")
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(8)
        main_layout.addWidget(self.label)
        main_layout.addStretch(1)

    def set_workflow_name(self, name: str):
        self._workflow_name = name
        display = name if name else "—"
        self.label.setText(f"Workflow: {display}")
