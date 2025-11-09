import os
import json
from PyQt5.QtCore import QStandardPaths


class Config(dict):
    def __init__(self, app_name: str = "KritaComfyUI-15347", filename: str = "config.json"):
        super().__init__()
        self._app_name = app_name
        self._filename = filename
        self._path = self._resolve_path()
        self._load()

    def _resolve_path(self) -> str:
        base_dir = QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation)
        app_dir = os.path.join(base_dir, self._app_name)
        os.makedirs(app_dir, exist_ok=True)
        return os.path.join(app_dir, self._filename)

    def _load(self) -> None:
        if os.path.exists(self._path):
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.update(data)
            except Exception:
                pass

    def save(self) -> None:
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.save()

    def __delitem__(self, key):
        super().__delitem__(key)
        self.save()

    @property
    def path(self) -> str:
        return self._path